"""
core/email.py — Resend-powered transactional email helpers.

All functions are no-op safe: if RESEND_API_KEY is not configured,
they log a warning and return without raising so app flow is never
blocked by a missing mail configuration.
"""

import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def _resend_client():
    """Return resend module if API key is configured, else None."""
    api_key = getattr(settings, "RESEND_API_KEY", "")
    if not api_key:
        logger.debug("RESEND_API_KEY not set — email skipped")
        return None
    try:
        import resend
        resend.api_key = api_key
        return resend
    except ImportError:
        logger.warning("resend package not installed")
        return None


FROM_ADDRESS = getattr(settings, "FROM_EMAIL", "Career Reality <hello@careerreality.in>")


# ---------------------------------------------------------------------------
# Newsletter welcome
# ---------------------------------------------------------------------------


def send_newsletter_welcome(email: str) -> bool:
    resend = _resend_client()
    if resend is None:
        return False
    try:
        resend.Emails.send(
            {
                "from": FROM_ADDRESS,
                "to": [email],
                "subject": "Welcome to Career Reality — Your first reality check",
                "html": _welcome_html(email),
            }
        )
        return True
    except Exception:
        logger.exception("send_newsletter_welcome failed for %s", email)
        return False


def _welcome_html(email: str) -> str:
    return f"""
<div style="font-family:system-ui,sans-serif;max-width:600px;margin:0 auto;color:#111;">
  <h2 style="border-bottom:2px solid #000;padding-bottom:8px;">Career Reality</h2>
  <p>You're subscribed. No spam, no motivational slides.</p>
  <p>Every week you'll get:</p>
  <ul>
    <li>Real salary ranges for Indian tech roles</li>
    <li>Layoff radar updates from the community</li>
    <li>One honest career decision framework</li>
  </ul>
  <p>While you're here — check your CTC reality:</p>
  <p><a href="https://www.careerreality.in/salary-calculator/"
        style="background:#000;color:#fff;padding:10px 20px;text-decoration:none;border-radius:4px;">
      CTC Decoder →
  </a></p>
  <hr style="margin:2rem 0;border:none;border-top:1px solid #eee;">
  <p style="font-size:12px;color:#999;">
    You signed up at careerreality.in with {email}.
    <a href="https://www.careerreality.in/newsletter/unsubscribe/?email={email}"
       style="color:#999;">Unsubscribe</a>
  </p>
</div>
"""


# ---------------------------------------------------------------------------
# Purchase confirmation / delivery
# ---------------------------------------------------------------------------


def send_purchase_confirmation(email: str, order) -> bool:
    resend = _resend_client()
    if resend is None:
        return False
    try:
        resend.Emails.send(
            {
                "from": FROM_ADDRESS,
                "to": [email],
                "subject": f"✓ Purchase confirmed — {order.product.name}",
                "html": _purchase_html(email, order),
            }
        )
        return True
    except Exception:
        logger.exception("send_purchase_confirmation failed for order %s", order.id)
        return False


def _purchase_html(email: str, order) -> str:
    is_subscription = order.product.product_type == "subscription_monthly"
    delivery_section = (
        """
  <p><strong>Your access is now active.</strong></p>
  <p>Log in to your <a href="https://www.careerreality.in/pro/dashboard/">Pro Dashboard</a>
     to access the full salary database, layoff alerts, and all premium tools.</p>
"""
        if is_subscription
        else """
  <p><strong>Your Exit Checklist is ready.</strong></p>
  <p>Download it here:
     <a href="https://www.careerreality.in/pro/exit-checklist/">
       Exit Checklist PDF →
     </a>
  </p>
  <p>This link is valid for 7 days.</p>
"""
    )

    return f"""
<div style="font-family:system-ui,sans-serif;max-width:600px;margin:0 auto;color:#111;">
  <h2 style="border-bottom:2px solid #000;padding-bottom:8px;">Career Reality</h2>
  <p>Payment confirmed. Order ID: <code>{order.razorpay_payment_id}</code></p>
  <p><strong>Product:</strong> {order.product.name}</p>
  <p><strong>Amount:</strong> ₹{order.amount_rupees}</p>
  {delivery_section}
  <hr style="margin:2rem 0;border:none;border-top:1px solid #eee;">
  <p style="font-size:12px;color:#999;">
    Receipt sent to {email}. Questions? Reply to this email.
  </p>
</div>
"""


# ---------------------------------------------------------------------------
# Weekly digest (called from cron)
# ---------------------------------------------------------------------------


def send_weekly_digest(subscribers: list[str], salary_count: int, layoff_count: int) -> int:
    """
    Send weekly digest to a list of email addresses.
    Returns the count of successfully sent emails.
    """
    resend = _resend_client()
    if resend is None:
        return 0

    sent = 0
    subject = f"Career Reality Weekly — {salary_count} new salary data points this week"
    for email in subscribers:
        try:
            resend.Emails.send(
                {
                    "from": FROM_ADDRESS,
                    "to": [email],
                    "subject": subject,
                    "html": _weekly_digest_html(email, salary_count, layoff_count),
                }
            )
            sent += 1
        except Exception:
            logger.exception("Weekly digest failed for %s", email)
    return sent


def _weekly_digest_html(email: str, salary_count: int, layoff_count: int) -> str:
    return f"""
<div style="font-family:system-ui,sans-serif;max-width:600px;margin:0 auto;color:#111;">
  <h2 style="border-bottom:2px solid #000;padding-bottom:8px;">Career Reality Weekly</h2>
  <p>Here's what happened this week in Indian tech careers:</p>
  <ul>
    <li><strong>{salary_count} new salary data points</strong> added to the community database</li>
    <li><strong>{layoff_count} layoff/freeze reports</strong> flagged across companies</li>
  </ul>
  <p>
    <a href="https://www.careerreality.in/salary-drop/"
       style="background:#000;color:#fff;padding:10px 20px;text-decoration:none;border-radius:4px;">
      See Salary Intelligence →
    </a>
  </p>
  <p style="margin-top:1.5rem;">
    <a href="https://www.careerreality.in/layoff-radar/">Layoff Radar</a> &nbsp;|&nbsp;
    <a href="https://www.careerreality.in/salary-calculator/">CTC Decoder</a> &nbsp;|&nbsp;
    <a href="https://www.careerreality.in/resignation-risk/">Risk Analyzer</a>
  </p>
  <hr style="margin:2rem 0;border:none;border-top:1px solid #eee;">
  <p style="font-size:12px;color:#999;">
    Sent to {email}.
    <a href="https://www.careerreality.in/newsletter/unsubscribe/?email={email}"
       style="color:#999;">Unsubscribe</a>
  </p>
</div>
"""


# ---------------------------------------------------------------------------
# Pro watchlist layoff alerts
# ---------------------------------------------------------------------------


STATUS_LABELS = {
    "freeze": "Hiring Freeze",
    "rumor": "Layoff Rumors",
    "layoff": "Active Layoffs",
}


def send_layoff_watchlist_alert(email: str, company, reports: list) -> bool:
    """Send a layoff alert email for a watched company."""
    resend = _resend_client()
    if resend is None:
        return False
    try:
        company_name = company.name if hasattr(company, "name") else str(company)
        subject = f"Layoff alert: {company_name} — new stability reports"
        resend.Emails.send(
            {
                "from": FROM_ADDRESS,
                "to": [email],
                "subject": subject,
                "html": _layoff_watchlist_html(email, company, reports),
            }
        )
        return True
    except Exception:
        logger.exception("send_layoff_watchlist_alert failed for %s", email)
        return False


def _layoff_watchlist_html(email: str, company, reports: list) -> str:
    company_name = company.name if hasattr(company, "name") else str(company)
    slug = getattr(company, "slug", "")
    company_url = (
        f"https://www.careerreality.in/companies/{slug}/"
        if slug
        else "https://www.careerreality.in/layoff-radar/"
    )

    rows = ""
    for report in reports:
        status_label = STATUS_LABELS.get(report.status, report.get_status_display())
        details = report.details[:200] if report.details else ""
        role_part = f" — {report.role_affected}" if report.role_affected else ""
        loc_part = f" ({report.location})" if report.location else ""
        detail_part = (
            f'<br><span style="color:#666;font-size:13px;">{details}</span>'
            if details
            else ""
        )
        rows += f"""
        <li style="margin-bottom:12px;">
          <strong>{status_label}</strong>{role_part}{loc_part}{detail_part}
        </li>
        """

    return f"""
<div style="font-family:system-ui,sans-serif;max-width:600px;margin:0 auto;color:#111;">
  <h2 style="border-bottom:2px solid #000;padding-bottom:8px;">Layoff Alert — {company_name}</h2>
  <p>New stability reports were submitted for a company on your Pro watchlist:</p>
  <ul>{rows}</ul>
  <p>
    <a href="{company_url}"
       style="background:#000;color:#fff;padding:10px 20px;text-decoration:none;border-radius:4px;">
      View {company_name} Profile →
    </a>
  </p>
  <p style="margin-top:1.5rem;">
    <a href="https://www.careerreality.in/layoff-radar/">Layoff Radar</a> &nbsp;|&nbsp;
    <a href="https://www.careerreality.in/accounts/dashboard/">Pro Dashboard</a>
  </p>
  <hr style="margin:2rem 0;border:none;border-top:1px solid #eee;">
  <p style="font-size:12px;color:#999;">
    Sent to {email} because you watch {company_name} on Career Reality Pro.
  </p>
</div>
"""
