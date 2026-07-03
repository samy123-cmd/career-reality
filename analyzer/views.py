import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST
from django.views.decorators.vary import vary_on_cookie
from django.utils.cache import patch_cache_control
from django.utils import timezone
from core.seo_pages import LAYOFF_RADAR, RESIGNATION_ANALYZER
from . import forms, logic, models
from .salary_access import CREDITS_PER_SUBMISSION, get_balance, unlock_salary_row
from .verification import apply_light_verification

COMPANY_TYPE_LABELS = dict(models.SalarySubmission.COMPANY_TYPES)

# Wizard Configuration
STEPS = {
    1: forms.Step1Form,
    2: forms.Step2Form,
    3: forms.Step3Form,
}

@cache_page(60 * 30)
@vary_on_cookie
def intro_view(request):
    """Landing page for the resignation risk analyzer."""
    methodology_last_updated = timezone.localdate().strftime('%B %d, %Y')
    seo = RESIGNATION_ANALYZER
    return render(request, 'analyzer/intro.html', {
        'og_title': seo.title,
        'og_description': seo.description,
        'twitter_title': seo.title,
        'twitter_description': seo.description,
        'methodology_last_updated': methodology_last_updated,
        'page_h1': seo.h1,
        'page_keywords': seo.keywords,
    })

def wizard_start_session(request):
    """
    Initializes a new session and redirects to step 1.
    Called via POST from intro page to ensure fresh start.
    """
    if request.method == 'POST':
        # Clear specific analyzer keys to reset
        # Note: keys were 'analyzer_step', 'analyzer_data' in original file?
        # Checking file content: yes 'analyzer_step', 'analyzer_data'.
        # I should stick to 'analyzer_*' or migrate to 'wizard_*'. 
        # The prompt implies 'wizard_start' name used in urls. 
        # I will use 'analyzer_*' keys to match existing view logic below.
        
        keys_to_clear = ['analyzer_step', 'analyzer_data', 'analyzer_complete', 'analyzer_logged']
        for key in keys_to_clear:
            if key in request.session:
                del request.session[key]
        
        # Set session expiry to 30 minutes (Hardening)
        request.session.set_expiry(1800)
        
        request.session['analyzer_step'] = 1
        request.session['analyzer_data'] = {}
        return redirect('wizard_step', step=1)
            
    # If GET, just go to intro
    return redirect('analyzer_home')

def wizard_step(request, step):
    """Generic step handler."""
    
    # Validation: Enforce sequential access
    current_step = request.session.get('analyzer_step', 1)
    if step > current_step:
        return redirect('wizard_step', step=current_step)
    
    FormClass = STEPS.get(step)
    if not FormClass:
        return redirect('wizard_start')

    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            # Save data to session
            data = request.session.get('analyzer_data', {})
            data.update(form.cleaned_data)
            request.session['analyzer_data'] = data
            
            # Advancing logic
            if step < 3:
                request.session['analyzer_step'] = step + 1
                return redirect('wizard_step', step=step + 1)
            else:
                # Final step completed
                request.session['analyzer_complete'] = True
                return redirect('wizard_result')
    else:
        # Pre-fill form if data exists (taking a step back)
        data = request.session.get('analyzer_data', {})
        form = FormClass(initial=data)

    return render(request, f'analyzer/step_{step}.html', {
        'form': form, 
        'step': step, 
        'total_steps': 3,
        'meta_robots': 'noindex, follow',
    })

def result_view(request):
    """
    Final Result Page.
    - Protected: Redirects to start if session invalid/incomplete.
    - Idempotent-ish: Calculates risk but doesn't re-log if already logged? 
      Actually, we just calculate. Logging happens here.
    """
    if not request.session.get('analyzer_complete'):
        return redirect('wizard_start')
        
    data = request.session.get('analyzer_data', {})
    
    # Calculate Risk
    calculator = logic.RiskCalculator()
    result = calculator.calculate(data)

    role_label        = dict(forms.copy.ROLE_LEVELS).get(data.get('role_level'), 'Unknown')
    company_label     = dict(forms.copy.COMPANY_TYPES).get(data.get('company_type'), 'Unknown')
    notice_label      = dict(forms.copy.NOTICE_PERIODS).get(data.get('notice_period'), 'Unknown')
    tenure_label      = dict(forms.copy.TENURE_BANDS).get(data.get('tenure_band'), 'Unknown')
    ctc_label         = dict(forms.copy.CTC_VS_MARKET).get(data.get('ctc_vs_market'), 'Unknown')
    performance_label = dict(forms.copy.PERFORMANCE_STATUS).get(data.get('performance_status'), 'Unknown')

    primary_action_map = {
        'high': "Document all communication and line up legal-safe exit options in the next 24 hours.",
        'medium': "Stabilize leverage first: gather documents, clarify terms in writing, and avoid verbal-only commitments.",
        'low': "Proceed with structured resignation steps and keep process evidence organized.",
    }

    methodology_last_updated = timezone.localdate().strftime('%B %d, %Y')
    
    # Analytics Logging (Privacy Safe)
    # Check if already logged to prevent duplicates on refresh
    if not request.session.get('analyzer_logged'):
        models.AssessmentLog.objects.create(
            risk_level=result['level'],
            scenario_type=data.get('current_situation', 'unknown'),
            has_offer=(data.get('has_offer') == 'yes'),
            tool_version="1.0"
        )
        request.session['analyzer_logged'] = True

        # Increment engagement counter on user profile
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                profile.assessments_count += 1
                profile.last_risk_level = result['level']
                profile.last_company_type = data.get('company_type', '')
                profile.save(update_fields=['assessments_count', 'last_risk_level', 'last_company_type'])
            except Exception:
                pass

    # LLM-powered personalized narrative (graceful fallback if no API key)
    from .llm import generate_risk_narrative
    llm_narrative = generate_risk_narrative(data, result)

    from django.conf import settings
    razorpay_key_id = getattr(settings, 'RAZORPAY_KEY_ID', '')

    title = f"Risk Result: {result.get('label', 'Assessment')} - Career Reality India"
    description = "Your resignation risk level with context and next steps based on common Indian employment patterns."
    return render(request, 'analyzer/result.html', {
        'result': result,
        'role_label': role_label,
        'company_label': company_label,
        'notice_label': notice_label,
        'tenure_label': tenure_label,
        'ctc_label': ctc_label,
        'performance_label': performance_label,
        'llm_narrative': llm_narrative,
        'razorpay_key_id': razorpay_key_id,
        'primary_action': primary_action_map.get(result['level'], primary_action_map['medium']),
        'methodology_last_updated': methodology_last_updated,
        'og_title': title,
        'og_description': description,
        'twitter_title': title,
        'twitter_description': description,
        'meta_robots': 'noindex, follow',
    })


@require_POST
def track_event_api(request):
    """Store privacy-safe funnel events for conversion and replay diagnostics."""
    allowed_events = {
        'landing_view',
        'analyze_submit',
        'analysis_rendered',
        'paywall_view',
        'upgrade_click',
        'upgrade_success',
        'return_visit_d7',
        'newsletter_cta_shown',
    }

    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'error': 'invalid_json'}, status=400)

    event_name = payload.get('event_name')
    if event_name not in allowed_events:
        return JsonResponse({'ok': False, 'error': 'invalid_event'}, status=400)

    metadata = payload.get('metadata', {})
    if not isinstance(metadata, dict):
        metadata = {}

    models.FunnelEventLog.objects.create(
        event_name=event_name,
        session_id=(payload.get('session_id') or '')[:64],
        page_path=(payload.get('page_path') or request.path)[:255],
        user_agent=(request.META.get('HTTP_USER_AGENT') or '')[:255],
        metadata=metadata,
    )

    return JsonResponse({'ok': True})

def submit_salary(request):
    """
    Handle anonymous salary submissions.
    Give-to-get: submitting a salary earns 3 unlock credits (or session unlock for anon users).
    """
    source = request.GET.get("source", "") or request.POST.get("source", "")

    if request.method == 'POST':
        form = forms.SalarySubmissionForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data

            # Attempt to match to a Company profile by name
            from companies.models import Company as CompanyModel
            company_obj = None
            raw_name = d.get('company_name', '').strip()
            if raw_name:
                company_obj = CompanyModel.objects.filter(
                    name__iexact=raw_name
                ).first()

            submission = models.SalarySubmission.objects.create(
                role=d['role'],
                experience_years=d['experience_years'],
                company_type=d['company_type'],
                ctc=d['ctc'],
                city=d['city'],
                tech_stack=d.get('tech_stack', ''),
                company=company_obj,
                company_name=raw_name,
                source=(d.get("source") or source or "")[:40],
            )
            apply_light_verification(
                submission,
                confirmed_payslip=d.get('confirm_payslip', False),
            )

            # ── Give-to-get: award salary unlock credits ──────────────────
            if request.user.is_authenticated:
                try:
                    profile = request.user.profile
                    profile.salary_submissions_count += 1
                    profile.salary_credits += CREDITS_PER_SUBMISSION
                    profile.save(update_fields=[
                        'salary_submissions_count', 'salary_credits'
                    ])
                except Exception:
                    pass
            else:
                # Anonymous users get a session-based unlock window
                request.session['salary_unlocks'] = (
                    request.session.get('salary_unlocks', 0) + CREDITS_PER_SUBMISSION
                )

            request.session['last_credits_earned'] = CREDITS_PER_SUBMISSION
            return redirect(reverse('salary_submit_success'))
    else:
        initial = {}
        if source:
            initial['source'] = source[:40]
        form = forms.SalarySubmissionForm(initial=initial)

    title = "Anonymous Salary Drop"
    description = "Submit an anonymous salary data point to improve Career Reality salary ranges and insights."
    return render(request, 'analyzer/submit_salary.html', {
        'form': form,
        'source': source,
        'og_title': title,
        'og_description': description,
        'twitter_title': title,
        'twitter_description': description,
        'meta_robots': 'noindex, follow',
    })

def salary_submit_success(request):
    credits_earned = request.session.pop('last_credits_earned', CREDITS_PER_SUBMISSION)
    title = "Submission Received - Career Reality India"
    description = "Thanks for contributing anonymous salary data. It helps improve salary reality checks for everyone."
    return render(request, 'analyzer/submit_success.html', {
        'og_title': title,
        'og_description': description,
        'twitter_title': title,
        'twitter_description': description,
        'meta_robots': 'noindex, follow',
        'credits_earned': credits_earned,
        'salary_credit_balance': get_balance(request),
    })


@require_POST
def unlock_salary(request, submission_id):
    """Unlock a single salary row using credits or free monthly previews."""
    from django.contrib import messages

    submission = models.SalarySubmission.objects.filter(pk=submission_id).first()
    if not submission:
        messages.error(request, "Salary record not found.")
        return redirect(request.META.get("HTTP_REFERER", "company_directory"))

    success, reason = unlock_salary_row(request, submission_id)
    if success:
        if reason == "credit":
            messages.success(request, "Salary unlocked using 1 credit.")
        elif reason == "preview":
            messages.success(request, "Salary unlocked using a free monthly preview.")
        elif reason == "pro":
            messages.success(request, "Salary unlocked (Pro access).")
    else:
        messages.warning(
            request,
            "No unlocks remaining. Submit your salary to earn 3 credits, or upgrade to Pro.",
        )

    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER", "company_directory")
    return redirect(next_url)
def salary_feed_api(request):
    """
    Returns last 20 verified (or all for now) salaries for the ticker.
    """
    import logging
    from django.http import JsonResponse
    logger = logging.getLogger(__name__)
    try:
        verified = list(
            models.SalarySubmission.objects.filter(
                verification_status="verified"
            ).values(
                'role', 'company_type', 'experience_years', 'ctc', 'city'
            ).order_by('-created_at')[:20]
        )
        pending_limit = max(0, 20 - len(verified))
        pending = list(
            models.SalarySubmission.objects.exclude(
                verification_status="verified"
            ).values(
                'role', 'company_type', 'experience_years', 'ctc', 'city'
            ).order_by('-created_at')[:pending_limit]
        )
        submissions = verified + pending
        data = [
            {
                'role': row['role'],
                'company': COMPANY_TYPE_LABELS.get(row['company_type'], row['company_type']),
                'exp': f"{row['experience_years']}y",
                'ctc': f"{row['ctc']/100000:.1f} LPA",
                'city': row['city'],
            }
            for row in submissions
        ]
        response = JsonResponse({'submissions': data})
        patch_cache_control(response, public=True, max_age=120, stale_while_revalidate=60)
        return response
    except Exception:
        logger.exception("salary_feed_api failed")
        response = JsonResponse({'error': 'Service temporarily unavailable.'}, status=500)
        patch_cache_control(response, no_store=True)
        return response

@cache_page(60 * 15)
def layoff_radar(request):
    """
    Dashboard showing company stability status.
    Aggregates reports to show 'Danger' vs 'Safe'.
    """
    from django.utils import timezone as tz
    from datetime import timedelta
    now = tz.now()
    yesterday = now - timedelta(hours=24)

    recent_reports = list(
        models.LayoffReport.objects.only(
            'company_name', 'status', 'role_affected', 'location', 'details', 'created_at'
        ).order_by('-created_at')[:50]
    )

    # Add a lightweight confidence score per report
    for report in recent_reports:
        score = 30
        if report.details:
            score += 20
        if report.status in ['freeze', 'rumor', 'layoff']:
            score += 10
        age_days = (now - report.created_at).days
        if age_days <= 7:
            score += 40
        elif age_days <= 30:
            score += 20
        report.confidence_score = min(score, 100)

    # Dynamic stats
    today_count  = sum(1 for r in recent_reports if r.created_at >= yesterday)
    total_count  = models.LayoffReport.objects.count()
    danger_total = models.LayoffReport.objects.filter(status__in=['freeze', 'rumor', 'layoff']).count()
    danger_pct   = round(danger_total / total_count * 100) if total_count else 0

    if danger_pct >= 60:
        risk_band        = "HIGH"
        risk_band_color  = "#d93025"
        market_volatility = danger_pct
    elif danger_pct >= 35:
        risk_band        = "ELEVATED"
        risk_band_color  = "#f59e0b"
        market_volatility = danger_pct
    else:
        risk_band        = "MODERATE"
        risk_band_color  = "#16a34a"
        market_volatility = danger_pct

    seo = LAYOFF_RADAR
    return render(request, 'analyzer/layoff_radar.html', {
        'reports': recent_reports,
        'today_count': today_count,
        'total_count': total_count,
        'risk_band': risk_band,
        'risk_band_color': risk_band_color,
        'market_volatility': market_volatility,
        'page_h1': seo.h1,
        'page_keywords': seo.keywords,
        'og_title': seo.title,
        'og_description': seo.description,
        'twitter_title': seo.title,
        'twitter_description': seo.description,
    })

def report_layoff(request):
    """
    Anonymous form to report company status.
    """
    if request.method == 'POST':
        form = forms.LayoffReportForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data

            from companies.models import Company as CompanyModel
            company_obj = None
            raw_name = d['company_name'].strip()
            if raw_name:
                company_obj = CompanyModel.objects.filter(
                    name__iexact=raw_name
                ).first()

            models.LayoffReport.objects.create(
                company_name=raw_name,
                company=company_obj,
                status=d['status'],
                role_affected=d.get('role_affected', ''),
                location=d.get('location', ''),
                details=d.get('details', ''),
            )
            from django.contrib import messages
            messages.success(request, f"Report for {d['company_name']} submitted. Thank you for helping the community.")
            return redirect('report_layoff')
        # Re-render with validation errors

    else:
        form = forms.LayoffReportForm()

    title = "Report Layoff Status - Career Reality India"
    description = "Anonymous, secure layoff and hiring freeze reports to help others assess company risk."
    return render(request, 'analyzer/report_layoff.html', {
        'form': form,
        'og_title': title,
        'og_description': description,
        'twitter_title': title,
        'twitter_description': description,
        'meta_robots': 'noindex, follow',
    })
