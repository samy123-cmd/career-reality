# Text Constants for Resignation Risk Analyzer

# --- CHOICES FOR FORMS ---

COMPANY_TYPES = [
    ('service', 'Service-based (IT services / consulting)'),
    ('product', 'Product company / startup'),
    ('mnc_captive', 'MNC captive'),
    ('small_indian', 'Small Indian firm (<100 employees)'),
]

ROLE_LEVELS = [
    ('ic', 'Individual contributor'),
    ('senior_ic', 'Senior IC / team lead'),
    ('manager', 'Manager or above'),
]

BOND_STATUS = [
    ('no_bond', 'No bond'),
    ('bond_unclear', 'Bond signed, unclear enforceability'),
    ('bond_penalty', 'Bond with stated penalty amount'),
]

NOTICE_PERIODS = [
    ('30_days', '30 days or less'),
    ('60_days', '60 days'),
    ('90_days', '90 days'),
    ('more_90', 'More than 90 days'),
]

CURRENT_SITUATION = [
    ('manager_bad', 'Manager asked me to resign'),
    ('hr_bad', 'HR warned about consequences'),
    ('unsafe', 'I want to resign but feel unsafe'),
    ('offer_hand', 'Offer in hand, worried about resigning'),
    ('evaluating', 'No pressure yet, just evaluating risk'),
]

OFFER_STATUS = [
    ('yes', 'Yes'),
    ('no', 'No'),
]

# --- RISKS & LABELS ---

RISK_LABELS = {
    'low': {
        'label': 'Low Risk',
        'color': 'green',
        'summary': 'Your situation fits within standard professional norms. Standard procedures should work.'
    },
    'medium': {
        'label': 'Medium Risk',
        'color': 'yellow',
        'summary': 'There are friction points in your profile that could complicate your exit.'
    },
    'high': {
        'label': 'High Risk',
        'color': 'red',
        'summary': 'Significant deviation from standard norms. High probability of resistance or escalation.'
    }
}

# --- LAYER 1: ROTATIONAL RISK REASONS ---
# 7 Linguistic Variants per Level (Semantic Equivalents)

RISK_REASON_VARIANTS = {
    'low': [
        "Your employment terms align with standard industry practices favoring a predictable exit.",
        "MNC-style frameworks typically prioritize compliance over individual retention pressure.",
        "Structural factors in your profile suggest a procedural rather than emotional response.",
        "Standard resignation inputs generally lead to a standard offboarding process.",
        "Your current leverage allows for a transition without significant organizational friction.",
        "Professionals with this profile rarely encounter blockers beyond standard administration.",
        "The combination of your notice period and role typically results in a clean relieve."
    ],
    'medium': [
        "Notice periods of this length naturally create friction points during the transition.",
        "Ambiguity in employment terms can often lead to delays in the final releasing stages.",
        "There are specific constraints in your profile that employers often use as leverage.",
        "While not critical, your situation contains triggers that typically slow down offboarding.",
        "The current inputs suggest an environment where policy enforcement may become rigid.",
        "Your profile sits in a grey area where outcomes often depend on managerial discretion.",
        "Service-based contracts often trigger standardized resistance patterns in this scenario."
    ],
    'high': [
        "Direct escalation signals indicate the organization is moving from procedure to retention tactics.",
        "Financial or legal constraints are frequently used here to delay relieving documents.",
        "When professional boundaries are crossed, standard resignation procedures often fail to function normally.",
        "The combination of high-friction inputs usually creates significant vulnerability to market shifts.",
        "Structural power imbalances in this scenario often lead to an escalated exit process.",
        "Your profile contains multiple triggers that typically result in a 'holding pattern' by HR.",
        "In similar profiles, the lack of an offer and long notice creates maximum exposure to pressure."
    ]
}

# --- LAYER 2: CONTEXTUAL EXPANSION (OPTIONAL) ---
# "Why situations like this often escalate"

EXPANSION_TEXT = {
    'low': "In standardized environments, resignation is treated as a routine administrative lifecycle event. HR teams in this bracket typically follow a playbook focused on compliance and asset recovery rather than retention through pressure. While individual managers may express dissatisfaction, the system itself usually prevents them from blocking a formal exit.",
    'medium': "Organizations often use 'grey area' tactics—like ambiguous bond clauses or verbal delays—to test an employee's resolve. This is rarely about legal enforcement and more about slowing down the exit to disrupt your joining plans. The friction is usually designed to be just frustrating enough to force a negotiation, without crossing into formal liability.",
    'high': "When specific triggers like HR warnings or actionable bonds are present, the organization often shifts focus from 'offboarding' to 'risk management'. This can lead to the silent withholding of documents or vaguely threatening communication. The goal in these scenarios is often to create enough uncertainty that the employee abandons their resignation or accepts unfavorable terms."
}

# --- WARNING BULLETS (CONTEXTUAL) ---

WARNINGS = {
    'bond_pressure': "Intimidation tactics regarding your bond amount/enforceability.",
    'notice_extension': "Pressure to extend notice period beyond contract terms.",
    'relieving_delay': "Delays in issuing relieving letter or experience documents.",
    'hr_escalation': "HR escalation without written records (verbal warnings).",
    'salary_leverage': "Holding back final settlement or F&F clearance.",
    'manager_hostility': "Immediate exclusion from projects or hostile daily interactions.",
    'market_risk': "Difficulty finding immediate placement with a long notice period."
}

# --- NEXT 7 DAYS ---

NEXT_STEPS_INTRO = "In similar situations, professionals often encounter:"

# --- DISCLAIMERS ---

DISCLAIMER_TEXT = """
This analysis does not tell you to resign or stay.
It highlights risks professionals typically encounter so you are not surprised later.
"""
