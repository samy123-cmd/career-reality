from . import copy


class RiskCalculator:
    """
    Score-based risk engine calibrated for India 2025.

    9 signals → 0–100 score → Low / Medium / High
    + specific, non-random risk reason and per-situation next steps.
    """

    VERSION = "v2.0"

    # Score contribution per signal value.
    # Calibrated against commonly reported Indian IT exit scenarios.
    SCORES = {
        'company_type': {
            'service':      10,   # Enforces 90-day notice + bonds aggressively
            'product':       5,   # Cleaner exits, buyout culture exists
            'mnc_captive':   4,   # Follows documented process, rarely litigates
            'startup':       9,   # Founder-dependent, can turn hostile quickly
            'small_indian': 22,   # Highest risk: arbitrary, delays, no HR process
        },
        'role_level': {
            'ic':         0,
            'senior_ic':  5,   # "No one else knows this" retention pressure
            'manager':    9,   # Knowledge monopoly, handover hostage risk
        },
        'tenure_band': {
            'less_6m': 20,   # Bond at max legal weight, probation status
            '6m_18m':  12,   # Bond still active in most service + startup contracts
            '18m_3y':   5,   # Bond likely served, notice still applies
            '3y_plus':  0,   # Bond done, experienced exit, stronger position
        },
        'bond_status': {
            'no_bond':      0,
            'bond_unclear': 15,   # Fear tactic — creates delay without legal weight
            'bond_penalty': 28,   # Can be deducted from F&F without asking
        },
        'notice_period': {
            '30_days':  0,
            '60_days': 10,
            '90_days': 22,   # Joining date math breaks — two-sided pressure
            'more_90': 30,
        },
        'current_situation': {
            'evaluating':  0,
            'offer_hand':  3,
            'manager_bad': 25,   # Active hostile environment
            'hr_bad':      38,   # Org in documentation / legal-defence mode
            'unsafe':      42,   # Overrides all — safety first
        },
        'has_offer': {
            'yes': -15,   # Strongest buffer: financial security + firm timeline
            'no':    0,
        },
        'ctc_vs_market': {
            'below':    -8,   # Moral leverage; employer has weaker retention case
            'at_market': 0,
            'above':     10,  # Employer fights harder; counter-offer likely
        },
        'performance_status': {
            'pip_managed': 22,   # Complex legal intersection with termination risk
            'warning':     12,   # HR documentation phase has started
            'good':         0,
            'star':        -5,   # Leverage in negotiation (but counter-offer trap)
        },
    }

    # Score thresholds
    LOW_MAX    = 34
    MEDIUM_MAX = 64
    # > MEDIUM_MAX = high

    _LABELS = {
        'low': {
            'label':   'Low Risk',
            'color':   'green',
            'summary': 'Your profile aligns with standard industry norms. Proceed with a structured, documented exit.',
        },
        'medium': {
            'label':   'Medium Risk',
            'color':   'yellow',
            'summary': 'Specific friction points exist that could complicate or delay your exit if not managed carefully.',
        },
        'high': {
            'label':   'High Risk',
            'color':   'red',
            'summary': 'Multiple active signals indicate your exit will face organised resistance. Every move needs to be deliberate.',
        },
    }

    _DISCLAIMER = (
        "This analysis reflects patterns from common Indian employment scenarios. "
        "It is not legal advice. Your outcome depends on your specific contract, state labour law, "
        "and company policies. When in doubt, consult a labour lawyer."
    )

    # -----------------------------------------------------------------------

    def calculate(self, data: dict) -> dict:
        score = self._score(data)
        level = self._level(score)
        return {
            'level':               level,
            'score':               score,
            'label':               self._LABELS[level]['label'],
            'color':               self._LABELS[level]['color'],
            'summary':             self._LABELS[level]['summary'],
            'risk_reason':         self._build_risk_reason(data, score, level),
            'specific_next_steps': self._build_next_steps(data, level),
            'warnings':            self._build_warnings(data, level),
            'profile_summary':     self._build_profile_summary(data),
            'disclaimer':          self._DISCLAIMER,
        }

    # -----------------------------------------------------------------------
    # Internal helpers
    # -----------------------------------------------------------------------

    def _score(self, data: dict) -> int:
        total = sum(
            self.SCORES[key].get(data.get(key, ''), 0)
            for key in self.SCORES
        )
        return max(0, min(100, total))

    def _level(self, score: int) -> str:
        if score <= self.LOW_MAX:
            return 'low'
        if score <= self.MEDIUM_MAX:
            return 'medium'
        return 'high'

    def _build_risk_reason(self, data: dict, score: int, level: str) -> str:
        company     = data.get('company_type', '')
        situation   = data.get('current_situation', '')
        bond        = data.get('bond_status', '')
        notice      = data.get('notice_period', '')
        performance = data.get('performance_status', '')
        offer       = data.get('has_offer', '')
        tenure      = data.get('tenure_band', '')

        # Highest-urgency situations first
        if situation == 'unsafe':
            return (
                "Workplace safety concerns override standard exit protocols. "
                "The organisation has crossed from professional norms into personal harm territory. "
                "Your priority must shift from clean offboarding to documenting incidents and getting legal protection first."
            )

        if situation == 'hr_bad':
            if bond == 'bond_penalty':
                return (
                    "HR has issued a formal warning AND you have an active financial bond — "
                    "these are the two strongest legal levers an Indian employer holds simultaneously. "
                    "The company is in documentation mode. Every communication you make from here "
                    "will be part of a paper trail, in your favour or against you depending on how you execute."
                )
            return (
                "HR has issued a formal warning, which means the organisation has shifted from retention "
                "mode to documentation mode — they are building a case. "
                "Verbal warnings with no written record are unenforceable, but the intent is clear: "
                "they are preparing for a contested exit."
            )

        if situation == 'manager_bad':
            if bond == 'bond_penalty':
                return (
                    "Your manager is directly pressuring you to resign while a financial bond creates "
                    "legal liability — this combination is a classic two-lever tactic in service companies and small firms. "
                    "Do not verbally agree to any timeline or amount before you know "
                    "the exact legal enforceability of your bond in your state."
                )
            return (
                "Direct pressure from a manager creates a hostile exit environment. "
                "The critical risk: verbal 'you should resign' conversations can be reframed as voluntary exits, "
                "affecting your F&F, PF claims, and experience letter wording. "
                "Nothing verbal. Everything in writing."
            )

        if performance == 'pip_managed':
            return (
                "Being on a PIP while planning resignation creates a legal intersection most people "
                "miss: the company may choose to terminate before your resignation is processed, "
                "which controls how your exit is classified on paper. "
                "Sequence of documents matters here more than letter of resignation timing."
            )

        if performance == 'warning':
            return (
                "A performance warning means HR has started documenting your file. "
                "This is the beginning of a formal process — it doesn't block your exit, "
                "but it means every step of your resignation is under higher scrutiny than a standard offboarding."
            )

        if bond == 'bond_penalty' and tenure in ('less_6m', '6m_18m'):
            return (
                "An active financial bond in the first 18 months is at its peak legal enforceability in India. "
                "IT service companies with documented training costs can deduct bond amounts from "
                "your Full & Final settlement without a court order. Know the exact number before you resign."
            )

        if notice in ('90_days', 'more_90') and company == 'service':
            return (
                "90-day notice at an IT service company is where most exit plans fall apart. "
                "Your joining date at a new employer will conflict with your notice window, "
                "creating simultaneous pressure from both sides. "
                "Notice buyout — paying 30–45 days of gross salary — is the standard resolution path in this scenario."
            )

        if notice in ('90_days', 'more_90') and company == 'small_indian':
            return (
                "A long notice period at a small Indian firm gives the company maximum leverage: "
                "they know you need your relieving letter, and delays of 30–90 days are common "
                "specifically because there is no HR process to enforce timelines. "
                "The goal is to create enough friction that you return or accept unfavourable exit terms."
            )

        if bond == 'bond_unclear':
            return (
                "An unclear bond clause is a deliberate design choice by the employer — "
                "ambiguity creates fear that they cannot create with a specific number. "
                "The vast majority of vague bond clauses are unenforceable in Indian courts, "
                "but without knowing that definitively, they function as effective psychological leverage."
            )

        if offer == 'no' and notice in ('90_days', 'more_90'):
            return (
                "Without an offer in hand and a 90-day+ notice period, "
                "resigning now would give your current employer 3+ months with maximum leverage and no competing timeline. "
                "Securing an offer before invoking the notice period is the single most important move."
            )

        # Level-specific catch-alls
        if level == 'low':
            if company == 'mnc_captive':
                return (
                    "MNC captive centres follow documented HR processes that are structurally harder to deviate from. "
                    "Standard resignation procedures work here — the system is designed for process compliance, "
                    "not individual retention pressure."
                )
            if offer == 'yes':
                return (
                    "Having an offer before resigning is your strongest single buffer. "
                    "It removes financial pressure, locks your timeline, and shifts negotiating leverage "
                    "firmly to your side. This is the cleanest exit profile."
                )
            return (
                "The structural factors that most commonly cause friction in Indian exits "
                "are not present at a significant level in your profile. "
                "A standard, documented resignation process should work within normal parameters."
            )

        return (
            f"Your profile carries a risk score of {score}/100. "
            "Multiple friction factors in your inputs compound each other — "
            "this is rarely about formal legal enforcement and almost always about "
            "using your dependency on their documents to slow or pressure the exit."
        )

    def _build_next_steps(self, data: dict, level: str) -> list:
        company     = data.get('company_type', '')
        situation   = data.get('current_situation', '')
        bond        = data.get('bond_status', '')
        notice      = data.get('notice_period', '')
        performance = data.get('performance_status', '')
        offer       = data.get('has_offer', '')
        tenure      = data.get('tenure_band', '')
        ctc         = data.get('ctc_vs_market', '')
        steps = []

        # ── Step 1: Most urgent action based on current situation ──────────
        if situation == 'unsafe':
            steps.append(
                "Document every incident before you do anything else — dates, times, witnesses, screenshots. "
                "Contact a labour lawyer or the National Commission for Women helpline (181) before making any formal resignation move. "
                "Safety considerations legally change what you are entitled to claim."
            )
        elif situation == 'hr_bad':
            steps.append(
                "Stop all verbal-only responses immediately. Reply to every HR message in writing: "
                "'As per our conversation on [date], my understanding is [X].' "
                "Verbal warnings without written records are legally unenforceable. "
                "You are creating your audit trail now — not later."
            )
        elif situation == 'manager_bad':
            steps.append(
                "Every verbal conversation with your manager now needs a written follow-up. "
                "After any call or in-person meeting, send an email: "
                "'As per our conversation today at [time], you indicated [X].' "
                "This converts verbal pressure into a timestamped document. Do this from today."
            )
        elif performance == 'pip_managed':
            steps.append(
                "Do not sign any PIP document without reading every clause. "
                "'Signing for acknowledgement' can legally bind you to improvement targets. "
                "If you plan to resign: submit your resignation letter before signing the PIP acknowledgement — "
                "sequence of documents controls how your exit is classified."
            )
        else:
            steps.append(
                "Pull out your original appointment letter today and re-read the exact wording of your notice period clause. "
                "Verbal HR statements about notice periods are frequently inaccurate. "
                "The appointment letter is the only document that legally governs your exit timeline — not what HR verbally told you."
            )

        # ── Step 2: Bond-specific ──────────────────────────────────────────
        if bond == 'bond_penalty':
            if company == 'small_indian':
                steps.append(
                    "Small Indian companies threaten bond enforcement but rarely follow through — "
                    "litigation costs more than most bond amounts. However, they will delay your relieving letter as leverage. "
                    "Plan for 30–60 days beyond your notice period before you receive your documents. "
                    "Do not accept a verbal 'we'll send it soon' — put a specific date in writing."
                )
            elif company == 'service' and tenure in ('less_6m', '6m_18m'):
                steps.append(
                    "IT service companies can and do deduct training bond amounts from your Full & Final settlement "
                    "without a court order, especially in the first 18 months. "
                    "Get the exact bond clause and amount in writing from HR before you resign. "
                    "If they cannot produce an itemised training cost breakdown, the amount is likely unenforceable."
                )
            else:
                steps.append(
                    "Confirm the exact bond penalty amount in writing from HR before resigning. "
                    "Verbal bond amounts are legally unenforceable — only signed, written figures matter. "
                    "If the clause says 'cost of training', ask HR for an itemised breakdown. "
                    "Most companies cannot produce it, which significantly weakens enforceability."
                )
        elif bond == 'bond_unclear':
            steps.append(
                "Get a one-hour consultation with a labour lawyer in your city (₹1,000–3,000) "
                "to assess whether your bond clause is enforceable in your state. "
                "Most vague bond clauses are not. Knowing this before you resign removes the biggest "
                "psychological lever the company holds over your decision timeline."
            )

        # ── Step 3: Notice period ──────────────────────────────────────────
        if notice in ('90_days', 'more_90'):
            if company == 'service':
                steps.append(
                    "90-day notice at an IT service company is negotiable via salary buyout. "
                    "Standard practice: offer 30–45 days of gross salary as buyout on the day you resign. "
                    "Most large service companies accept this because an unmotivated employee on notice is a team and delivery liability. "
                    "Calculate your 45-day gross salary now — have the figure ready for day 1."
                )
            elif company == 'product':
                steps.append(
                    "Product companies are the most flexible about notice buyouts. "
                    "Approach your direct manager first — not HR — with a specific joining date from your offer. "
                    "Frame it as a clean handover with a buyout number attached. "
                    "The manager's sign-off moves faster than the HR process."
                )
            else:
                steps.append(
                    "Notice periods longer than 60 days are negotiable in most Indian companies. "
                    "Formula: (notice days − 30) × daily gross salary = buyout offer. "
                    "Propose this in your resignation letter directly — it shows professionalism "
                    "and sets a concrete alternative to a drawn-out handover."
                )
        elif notice == '60_days':
            steps.append(
                "60-day notice is frequently negotiable to 30–45 days with a partial buyout. "
                "If your new employer has a specific joining date, present it to HR and propose a buyout for the gap. "
                "A disengaged employee in the last 30 days creates more organisational cost than the buyout amount — "
                "most companies know this and agree."
            )

        # ── Step 4: Offer strategy ─────────────────────────────────────────
        if offer == 'yes':
            steps.append(
                "Do not share your offer letter or new employer's name with anyone at your current company until your last day. "
                "This information will be used for counter-offers, delay tactics, or early system access revocation. "
                "You only need to share your 'proposed date of joining new organisation' if formally asked in writing."
            )
        elif offer == 'no' and situation not in ('hr_bad', 'unsafe', 'manager_bad'):
            steps.append(
                "Without an offer letter, avoid making any formal resignation move — even mentally. "
                "Your negotiating position is near-zero once you resign without an alternative. "
                "Your current job is your most powerful search asset. Use it."
            )

        # ── Step 5: Performance-specific ──────────────────────────────────
        if performance == 'star':
            steps.append(
                "Top performers are most vulnerable to counter-offer manipulation. "
                "Before your exit conversation, write down your three non-negotiables "
                "(designation, CTC number, team/domain scope). "
                "Counter-offers that resolve the stated reason in 3 months almost always revert — "
                "the structural issue remains unchanged."
            )
        elif performance == 'pip_managed':
            steps.append(
                "Confirm with HR in writing that your exit will be recorded as 'voluntary resignation' "
                "and not 'terminated with cause'. This distinction affects background verification at every future employer. "
                "Get this confirmation before your last day — after you leave, the record is set."
            )
        elif performance == 'warning':
            steps.append(
                "A performance warning on file means future BGV might surface it. "
                "Get written confirmation from HR that your exit is clean — no disciplinary actions pending at the time of leaving. "
                "One email asking for 'standard exit confirmation' is all you need."
            )

        # ── Step 6: CTC context ────────────────────────────────────────────
        if ctc == 'above':
            steps.append(
                "Being above market rate means a counter-offer is very likely. "
                "Decide your number in advance: what would make leaving feel like a financial mistake? "
                "If their counter-offer doesn't exceed that number by a meaningful margin, "
                "the decision is already made — you're just executing it."
            )

        # ── Always last: documentation checklist ──────────────────────────
        steps.append(
            "Last-day checklist — non-negotiable: "
            "(1) Download all payslips and increment letters from HRMS. "
            "(2) Screenshot your work inbox and any important project emails. "
            "(3) Confirm your PF UAN is active and shows the current employer's PF number. "
            "(4) Get physical or email copies of your appointment letter and last 3 appraisals. "
            "System and email access is revoked the moment you leave — often without warning."
        )

        return steps[:6]

    def _build_warnings(self, data: dict, level: str) -> list:
        company     = data.get('company_type', '')
        situation   = data.get('current_situation', '')
        bond        = data.get('bond_status', '')
        notice      = data.get('notice_period', '')
        performance = data.get('performance_status', '')
        offer       = data.get('has_offer', '')
        tenure      = data.get('tenure_band', '')
        warnings = []

        if bond == 'bond_penalty':
            warnings.append("Bond deduction: company may deduct penalty directly from F&F without a court order.")
        elif bond == 'bond_unclear':
            warnings.append("Ambiguous bond: used as psychological leverage even when legally unenforceable.")

        if notice in ('90_days', 'more_90'):
            warnings.append("Long notice: creates simultaneous pressure from current employer and new joining deadline.")

        if situation == 'hr_bad':
            warnings.append("HR escalation: org is in documentation mode — treat every interaction as a legal record.")
        elif situation == 'manager_bad':
            warnings.append("Hostile manager: verbal resignations can be reframed — never resign verbally first.")
        elif situation == 'unsafe':
            warnings.append("Safety risk: standard offboarding is secondary — personal protection and documentation first.")

        if company == 'small_indian':
            warnings.append("Small firm: relieving letter delays of 30–90 days are common, blocking BGV at new employer.")

        if performance == 'pip_managed':
            warnings.append("PIP status: company may attempt to terminate before your resignation is processed to control exit classification.")

        if offer == 'no' and situation not in ('hr_bad', 'unsafe'):
            warnings.append("No offer yet: leverage drops to near-zero once you formally resign.")

        if tenure == 'less_6m' and bond != 'no_bond':
            warnings.append("First 6 months + bond: peak window for bond enforcement — highest legal risk period.")

        return warnings[:5]

    def _build_profile_summary(self, data: dict) -> str:
        company_labels = dict(copy.COMPANY_TYPES)
        role_labels    = dict(copy.ROLE_LEVELS)
        tenure_labels  = dict(copy.TENURE_BANDS)
        company = company_labels.get(data.get('company_type', ''), 'an unspecified company')
        role    = role_labels.get(data.get('role_level', ''), 'Professional')
        tenure  = tenure_labels.get(data.get('tenure_band', ''), 'unspecified tenure')
        return f"{role} · {company} · {tenure} at this company"

