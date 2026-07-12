import hashlib
import hmac
import json
import logging
import uuid

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Order, Product, Subscription

logger = logging.getLogger(__name__)


def _razorpay_client():
    """Return a Razorpay client or None if keys are not configured."""
    key_id = getattr(settings, "RAZORPAY_KEY_ID", "")
    key_secret = getattr(settings, "RAZORPAY_KEY_SECRET", "")
    if not key_id or not key_secret:
        return None
    try:
        import razorpay
        return razorpay.Client(auth=(key_id, key_secret))
    except ImportError:
        logger.warning("razorpay package not installed")
        return None


@require_POST
def create_order(request):
    """
    POST /payments/create-order/
    Body: { "product_slug": "exit_checklist" }
    Returns: { "ok": true, "razorpay_order_id": "...", "amount": 9900, "key_id": "..." }
    """
    try:
        body = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "invalid_json"}, status=400)

    product_slug = (body.get("product_slug") or "").strip()
    if not product_slug:
        return JsonResponse({"ok": False, "error": "product_slug_required"}, status=400)

    try:
        product = Product.objects.get(slug=product_slug, is_active=True)
    except Product.DoesNotExist:
        return JsonResponse({"ok": False, "error": "product_not_found"}, status=404)

    client = _razorpay_client()
    if client is None:
        return JsonResponse(
            {"ok": False, "error": "payment_gateway_not_configured"},
            status=503,
        )

    receipt = str(uuid.uuid4())[:40]
    rz_order = client.order.create(
        {
            "amount": product.price_paise,
            "currency": "INR",
            "receipt": receipt,
            "notes": {"product_slug": product_slug, "site": "careerreality.in"},
        }
    )

    # Persist order in pending state
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        product=product,
        razorpay_order_id=rz_order["id"],
        amount_paise=product.price_paise,
        session_id=(body.get("session_id") or "")[:100],
        email=(body.get("email") or "")[:254],
    )

    return JsonResponse(
        {
            "ok": True,
            "razorpay_order_id": rz_order["id"],
            "order_uuid": str(order.id),
            "amount": product.price_paise,
            "currency": "INR",
            "key_id": settings.RAZORPAY_KEY_ID,
            "product_name": product.name,
            "product_description": product.short_description,
        }
    )


@require_POST
def verify_payment(request):
    """
    POST /payments/verify/
    Body: {
        "razorpay_order_id": "...",
        "razorpay_payment_id": "...",
        "razorpay_signature": "...",
        "email": "user@example.com"  (optional, for anonymous)
    }
    """
    try:
        body = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "invalid_json"}, status=400)

    rz_order_id = (body.get("razorpay_order_id") or "").strip()
    rz_payment_id = (body.get("razorpay_payment_id") or "").strip()
    rz_signature = (body.get("razorpay_signature") or "").strip()
    email = (body.get("email") or "")[:254].strip()

    if not all([rz_order_id, rz_payment_id, rz_signature]):
        return JsonResponse({"ok": False, "error": "missing_fields"}, status=400)

    client = _razorpay_client()
    if client is None:
        return JsonResponse({"ok": False, "error": "payment_gateway_not_configured"}, status=503)

    # Verify signature (critical security check)
    try:
        client.utility.verify_payment_signature(
            {
                "razorpay_order_id": rz_order_id,
                "razorpay_payment_id": rz_payment_id,
                "razorpay_signature": rz_signature,
            }
        )
    except Exception:
        logger.warning("Razorpay signature verification failed for order %s", rz_order_id)
        return JsonResponse({"ok": False, "error": "signature_invalid"}, status=400)

    # Fetch and update the pending order atomically to prevent race conditions
    try:
        with transaction.atomic():
            order = Order.objects.select_for_update().get(
                razorpay_order_id=rz_order_id, status="pending"
            )
            order.razorpay_payment_id = rz_payment_id
            order.razorpay_signature = rz_signature
            order.status = "paid"
            if email and not order.email:
                order.email = email
            order.delivered_at = timezone.now()
            order.save(update_fields=["razorpay_payment_id", "razorpay_signature", "status", "email", "delivered_at"])

            # If this is a subscription product, create the Subscription + update profile
            if order.product.product_type in ("subscription_monthly", "subscription_annual"):
                _activate_subscription(order)
    except Order.DoesNotExist:
        return JsonResponse({"ok": False, "error": "order_not_found"}, status=404)

    # Send confirmation email (outside transaction — non-critical)
    _send_delivery_email(order)

    return JsonResponse(
        {
            "ok": True,
            "message": "Payment verified. Check your email for next steps.",
            "product_type": order.product.product_type,
        }
    )


def _activate_subscription(order):
    """Create a subscription and update the user's profile tier."""
    from datetime import timedelta

    user = order.user
    if user is None:
        return

    now = timezone.now()
    if order.product.product_type == "subscription_annual":
        expires_at = now + timedelta(days=365)
    else:
        expires_at = now + timedelta(days=30)

    tier = "pro"
    if "team" in order.product.slug:
        tier = "team"

    Subscription.objects.create(
        user=user,
        tier=tier,
        status="active",
        started_at=now,
        expires_at=expires_at,
        order=order,
    )

    # Update UserProfile
    try:
        profile = user.profile
        profile.tier = tier
        profile.subscription_expires_at = expires_at
        profile.save(update_fields=["tier", "subscription_expires_at"])
    except Exception:
        pass


def _send_delivery_email(order):
    """Send purchase confirmation + delivery via Resend."""
    try:
        from core.email import send_purchase_confirmation
        recipient = order.email or (order.user.email if order.user else None)
        if recipient:
            send_purchase_confirmation(recipient, order)
    except Exception:
        logger.exception("Failed to send delivery email for order %s", order.id)


@csrf_exempt
@require_POST
def razorpay_webhook(request):
    """
    Razorpay webhook endpoint for server-side payment confirmation.
    Provides redundancy in case client-side verify_payment call fails.
    """
    webhook_secret = getattr(settings, "RAZORPAY_WEBHOOK_SECRET", "")
    if not webhook_secret:
        logger.warning("RAZORPAY_WEBHOOK_SECRET not configured — webhook rejected")
        return JsonResponse({"ok": False, "error": "webhook_not_configured"}, status=503)

    received_signature = request.headers.get("X-Razorpay-Signature", "")
    expected = hmac.new(
        webhook_secret.encode(),
        request.body,
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(expected, received_signature):
        logger.error("SECURITY: Invalid Razorpay webhook signature")
        return JsonResponse({"ok": False}, status=400)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False}, status=400)

    event = payload.get("event", "")
    if event == "payment.captured":
        rz_order_id = (
            payload.get("payload", {})
            .get("payment", {})
            .get("entity", {})
            .get("order_id", "")
        )
        if rz_order_id:
            Order.objects.filter(
                razorpay_order_id=rz_order_id, status="pending"
            ).update(status="paid", delivered_at=timezone.now())

    return JsonResponse({"ok": True})


@require_GET
def pricing(request):
    """Public pricing page."""
    from core.cache_utils import get_social_proof_counts

    products = Product.objects.filter(is_active=True).order_by("price_paise")
    social_proof = get_social_proof_counts()
    return render(
        request,
        "payments/pricing.html",
        {
            "products": products,
            "razorpay_key_id": getattr(settings, "RAZORPAY_KEY_ID", ""),
            "salary_count": social_proof.get("salary_count", "0"),
            "layoff_count": social_proof.get("layoff_count", "0"),
            "assessment_count": social_proof.get("assessment_count", "0"),
            "og_title": "Career Reality Pro — Salary Intelligence & Career Tools",
            "og_description": "Get access to India's most honest salary database, layoff alerts, and personalized exit checklists.",
        },
    )


def escape_roadmap(request):
    """Dedicated paywall landing page for the Personalised Escape Roadmap product."""
    role = request.GET.get("role", "dev")
    stack = request.GET.get("stack", "web")
    try:
        score = int(request.GET.get("score", "0"))
    except (ValueError, TypeError):
        score = 0

    return render(request, "payments/escape_roadmap.html", {
        "role": role,
        "stack": stack,
        "score": score,
        "razorpay_key_id": getattr(settings, "RAZORPAY_KEY_ID", ""),
        "og_title": "Your Personalised Escape Roadmap — Career Reality",
        "og_description": "Get your complete, role-specific step-by-step escape plan out of service company hell. One-time ₹199.",
    })
