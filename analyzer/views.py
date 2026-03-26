from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.utils.cache import patch_cache_control
from . import forms, logic, models

COMPANY_TYPE_LABELS = dict(models.SalarySubmission.COMPANY_TYPES)

# Wizard Configuration
STEPS = {
    1: forms.Step1Form,
    2: forms.Step2Form,
    3: forms.Step3Form,
}

def intro_view(request):
    """
    Landing page for the analyzer.
    Static, indexable content + Start button.
    """
    title = "Career Risk Analyzer - Career Reality India"
    description = "Answer 6 questions to estimate career risk and get a reality-first action plan."
    return render(request, 'analyzer/intro.html', {
        'og_title': title,
        'og_description': description,
        'twitter_title': title,
        'twitter_description': description,
        'meta_robots': 'noindex, follow',
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
    
    title = f"Risk Result: {result.get('label', 'Assessment')} - Career Reality India"
    description = "Your resignation risk level with context and next steps based on common Indian employment patterns."
    return render(request, 'analyzer/result.html', {
        'result': result,
        'og_title': title,
        'og_description': description,
        'twitter_title': title,
        'twitter_description': description,
        'meta_robots': 'noindex, follow',
    })

def submit_salary(request):
    """
    Handle anonymous salary submissions.
    """
    error = None
    if request.method == 'POST':
        form = forms.SalarySubmissionForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            models.SalarySubmission.objects.create(
                role=d['role'],
                experience_years=d['experience_years'],
                company_type=d['company_type'],
                ctc=d['ctc'],
                city=d['city'],
                tech_stack=d.get('tech_stack', ''),
            )
            return redirect(reverse('salary_submit_success'))
        error = "Invalid data"
    else:
        form = forms.SalarySubmissionForm()

    title = "Anonymous Salary Drop"
    description = "Submit an anonymous salary data point to improve Career Reality salary ranges and insights."
    return render(request, 'analyzer/submit_salary.html', {
        'form': form,
        'og_title': title,
        'og_description': description,
        'twitter_title': title,
        'twitter_description': description,
        'meta_robots': 'noindex, follow',
        'error': error,
    })

def salary_submit_success(request):
    title = "Submission Received - Career Reality India"
    description = "Thanks for contributing anonymous salary data. It helps improve salary reality checks for everyone."
    return render(request, 'analyzer/submit_success.html', {
        'og_title': title,
        'og_description': description,
        'twitter_title': title,
        'twitter_description': description,
        'meta_robots': 'noindex, follow',
    })
def salary_feed_api(request):
    """
    Returns last 20 verified (or all for now) salaries for the ticker.
    """
    import logging
    from django.http import JsonResponse
    logger = logging.getLogger(__name__)
    try:
        # For now, return all recent submissions. In prod, filter by is_verified=True
        submissions = models.SalarySubmission.objects.values(
            'role', 'company_type', 'experience_years', 'ctc', 'city'
        ).order_by('-created_at')[:20]
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

def layoff_radar(request):
    """
    Dashboard showing company stability status.
    Aggregates reports to show 'Danger' vs 'Safe'.
    """
    # Simple aggregation for V1: Get recent reports
    recent_reports = list(
        models.LayoffReport.objects.only(
            'company_name', 'status', 'role_affected', 'location', 'details', 'created_at'
        ).order_by('-created_at')[:50]
    )

    # Add a lightweight confidence score per report
    from django.utils import timezone
    now = timezone.now()
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
    
    # In V2, we would group by company_name and calculate a score.
    # For now, just list them.
    
    title = "Indian Tech Layoff Radar (2026)"
    description = "Crowdsourced layoff alerts and hiring freeze updates for Indian IT. Check if your company is safe and report anonymously."
    return render(request, 'analyzer/layoff_radar.html', {
        'reports': recent_reports,
        'meta_robots': 'noindex, follow',
        'og_title': title,
        'og_description': description,
        'twitter_title': title,
        'twitter_description': description,
    })

def report_layoff(request):
    """
    Anonymous form to report company status.
    """
    if request.method == 'POST':
        form = forms.LayoffReportForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            models.LayoffReport.objects.create(
                company_name=d['company_name'],
                status=d['status'],
                role_affected=d.get('role_affected', ''),
                location=d.get('location', ''),
                details=d.get('details', ''),
            )
            return redirect('layoff_radar')
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
