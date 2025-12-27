from django.shortcuts import render, redirect
from django.urls import reverse
from . import forms, logic, models

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
    return render(request, 'analyzer/intro.html')

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
        'total_steps': 3
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
    
    return render(request, 'analyzer/result.html', {
        'result': result
    })
