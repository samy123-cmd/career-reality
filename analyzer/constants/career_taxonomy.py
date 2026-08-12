"""Cross-discipline role, industry, and city taxonomy for CareerReality features."""

from __future__ import annotations

ROLE_CATEGORIES: dict[str, tuple[str, ...]] = {
    "Technology": (
        "Software Engineer",
        "Data Engineer",
        "Data Scientist",
        "ML / AI Engineer",
        "Cloud Engineer",
        "DevOps Engineer",
        "Cybersecurity Analyst",
        "QA Engineer",
        "Solution Architect",
        "ERP / SAP Consultant",
        "Salesforce / CRM Consultant",
        "Business Intelligence Analyst",
        "Analytics Engineer",
        "Product Manager",
        "Program Manager",
        "Project Manager",
        "UX / UI Designer",
        "IT Support Specialist",
        "Infrastructure Engineer",
    ),
    "Business & Finance": (
        "Financial Analyst",
        "Chartered Accountant",
        "Investment Banking Analyst",
        "Operations Manager",
        "Business Analyst",
        "Management Consultant",
        "Procurement Manager",
        "Legal Counsel",
    ),
    "Sales & Marketing": (
        "Sales Manager",
        "Account Executive",
        "Digital Marketing Manager",
        "Brand Manager",
        "Customer Success Manager",
    ),
    "HR & People": (
        "HR Business Partner",
        "Talent Acquisition Specialist",
        "People Analytics Analyst",
        "Learning & Development Manager",
    ),
    "Healthcare & Manufacturing": (
        "Healthcare Administrator",
        "Clinical Research Associate",
        "Production Manager",
        "Supply Chain Manager",
        "Quality Assurance Manager",
    ),
    "Other": (
        "Administrative Officer",
        "Education Professional",
        "Other Professional Role",
    ),
}

ROLE_ALIASES: dict[str, str] = {
    "sde": "Software Engineer",
    "developer": "Software Engineer",
    "backend": "Software Engineer",
    "frontend": "Software Engineer",
    "full stack": "Software Engineer",
    "data analyst": "Business Intelligence Analyst",
    "pm": "Product Manager",
    "po": "Product Manager",
    "ba": "Business Analyst",
    "hr": "HR Business Partner",
    "recruiter": "Talent Acquisition Specialist",
    "ca": "Chartered Accountant",
    "qa": "QA Engineer",
    "sdet": "QA Engineer",
    "devops": "DevOps Engineer",
    "ml engineer": "ML / AI Engineer",
    "ai engineer": "ML / AI Engineer",
}

INDUSTRY_CHOICES: tuple[tuple[str, str], ...] = (
    ("", "Select industry (optional)"),
    ("technology", "Technology / IT"),
    ("finance", "Finance & Banking"),
    ("consulting", "Consulting"),
    ("healthcare", "Healthcare"),
    ("manufacturing", "Manufacturing"),
    ("retail", "Retail & E-commerce"),
    ("telecom", "Telecom"),
    ("education", "Education"),
    ("other", "Other"),
)

CITY_CHOICES: tuple[tuple[str, str], ...] = (
    ("Bengaluru", "Bengaluru"),
    ("Hyderabad", "Hyderabad"),
    ("Pune", "Pune"),
    ("Mumbai", "Mumbai"),
    ("Delhi NCR", "Delhi NCR"),
    ("Chennai", "Chennai"),
    ("Kolkata", "Kolkata"),
    ("Ahmedabad", "Ahmedabad"),
    ("Remote", "Remote / WFH"),
    ("Other", "Other city"),
)

CITY_ALIASES = {
    "bangalore": "Bengaluru",
    "bengaluru": "Bengaluru",
    "blr": "Bengaluru",
    "hyd": "Hyderabad",
    "hyderabad": "Hyderabad",
    "pune": "Pune",
    "mumbai": "Mumbai",
    "delhi": "Delhi NCR",
    "ncr": "Delhi NCR",
    "gurgaon": "Delhi NCR",
    "gurugram": "Delhi NCR",
    "noida": "Delhi NCR",
    "chennai": "Chennai",
    "kolkata": "Kolkata",
    "remote": "Remote",
    "wfh": "Remote",
}


def all_roles_flat() -> list[tuple[str, str]]:
    """Return (value, label) pairs for select widgets with optgroups handled separately."""
    roles = []
    for category, items in ROLE_CATEGORIES.items():
        for role in items:
            roles.append((role, role))
    return roles


def role_choices_grouped() -> list[tuple[str, list[tuple[str, str]]]]:
    return [(cat, [(r, r) for r in roles]) for cat, roles in ROLE_CATEGORIES.items()]


def normalize_role(raw: str) -> str:
    key = raw.strip().lower()
    if not key:
        return "Software Engineer"
    if key in ROLE_ALIASES:
        return ROLE_ALIASES[key]
    for category_roles in ROLE_CATEGORIES.values():
        for role in category_roles:
            if role.lower() == key or key in role.lower() or role.lower() in key:
                return role
    return raw.strip()


def normalize_city(raw: str) -> str:
    key = raw.strip().lower()
    return CITY_ALIASES.get(key, raw.strip() or "Bengaluru")


def role_search_terms(role: str) -> list[str]:
    """Terms for DB/editorial matching."""
    norm = normalize_role(role)
    terms = [norm.lower(), norm.split()[0].lower()]
    for alias, canonical in ROLE_ALIASES.items():
        if canonical == norm:
            terms.append(alias)
    return list(dict.fromkeys(terms))
