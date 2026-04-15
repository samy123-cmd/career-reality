# analyzer/copy.py — Career Reality India — Resignation Risk Analyzer
# Choice tuples for forms and display labels.

# ---------------------------------------------------------------------------
# FORM CHOICES
# ---------------------------------------------------------------------------

COMPANY_TYPES = [
    ('service',      'IT Services / Consulting (TCS, Infy, Wipro, HCL tier)'),
    ('product',      'Indian Product Company (Swiggy, Zomato, CRED tier)'),
    ('mnc_captive',  'MNC Captive / Global Delivery Centre'),
    ('startup',      'Startup (Series A or earlier)'),
    ('small_indian', 'Small Indian Firm (<100 employees)'),
]

ROLE_LEVELS = [
    ('ic',        'Individual Contributor (no direct reports)'),
    ('senior_ic', 'Senior IC / Tech Lead / Team Lead'),
    ('manager',   'Manager, Sr. Manager or above'),
]

TENURE_BANDS = [
    ('less_6m', 'Less than 6 months'),
    ('6m_18m',  '6 months to 18 months'),
    ('18m_3y',  '18 months to 3 years'),
    ('3y_plus', 'More than 3 years'),
]

BOND_STATUS = [
    ('no_bond',      'No bond signed'),
    ('bond_unclear', 'Bond signed — not sure if enforceable'),
    ('bond_penalty', 'Bond with a specific penalty amount'),
]

NOTICE_PERIODS = [
    ('30_days', '30 days or less'),
    ('60_days', '60 days'),
    ('90_days', '90 days'),
    ('more_90', 'More than 90 days'),
]

CTC_VS_MARKET = [
    ('below',     "Below market — I know I'm underpaid"),
    ('at_market', 'Roughly at market rate'),
    ('above',     'Above market — well paid for my role'),
]

CURRENT_SITUATION = [
    ('evaluating',  'No pressure — just evaluating my options'),
    ('offer_hand',  'Have an offer, worried about the resignation process'),
    ('manager_bad', 'My manager has asked me to resign'),
    ('hr_bad',      'HR has warned me about consequences'),
    ('unsafe',      'I feel unsafe or threatened at work'),
]

PERFORMANCE_STATUS = [
    ('star',        'Top performer / on a critical project'),
    ('good',        'Good standing — no performance issues'),
    ('warning',     'Received a performance warning recently'),
    ('pip_managed', 'On PIP or actively being managed out'),
]

OFFER_STATUS = [
    ('yes', 'Yes, I have an offer letter'),
    ('no',  'No offer yet'),
]
