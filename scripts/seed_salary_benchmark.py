"""
scripts/seed_salary_benchmark.py

Seeds 100 realistic anonymous salary data points to bootstrap the
career intelligence database. Run once in production via:

    python manage.py shell < scripts/seed_salary_benchmark.py

or:

    python scripts/seed_salary_benchmark.py
"""

import os
import sys
import django
from pathlib import Path

# Allow running directly from CLI
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ.setdefault("SECRET_KEY", "seed-script-key")
os.environ.setdefault("DEBUG", "True")

django.setup()

from analyzer.models import SalarySubmission  # noqa: E402

SEED_DATA = [
    # (role, exp_years, company_type, ctc_inr, city, tech_stack)
    # --- Service Companies ---
    ("Software Engineer", 2.0, "service", 700000, "Bengaluru", "Java, Spring Boot"),
    ("Software Engineer", 3.5, "service", 950000, "Hyderabad", "Python, Django"),
    ("Senior Software Engineer", 5.0, "service", 1400000, "Bengaluru", "Java, Microservices, AWS"),
    ("Senior Software Engineer", 6.0, "service", 1600000, "Pune", "C#, .NET, Azure"),
    ("Technical Lead", 8.0, "service", 2000000, "Bengaluru", "Java, AWS, Kubernetes"),
    ("Technical Lead", 9.0, "service", 2200000, "Chennai", "Python, ML, GCP"),
    ("Project Manager", 10.0, "service", 2500000, "Hyderabad", "PMP, Agile"),
    ("Data Analyst", 2.5, "service", 750000, "Pune", "SQL, Excel, Tableau"),
    ("Data Analyst", 4.0, "service", 1100000, "Bengaluru", "Python, SQL, Power BI"),
    ("QA Engineer", 3.0, "service", 700000, "Chennai", "Selenium, Java, JIRA"),
    ("QA Engineer", 5.5, "service", 1100000, "Hyderabad", "Cypress, REST Assured, Python"),
    ("Business Analyst", 4.0, "service", 1200000, "Bengaluru", "SQL, Excel, Agile"),
    ("DevOps Engineer", 4.0, "service", 1300000, "Bengaluru", "AWS, Docker, Jenkins"),
    ("Cloud Engineer", 5.0, "service", 1600000, "Hyderabad", "AWS, Terraform, Kubernetes"),
    # --- Product Companies ---
    ("Software Engineer", 2.0, "product", 1400000, "Bengaluru", "React, Node.js"),
    ("Software Engineer", 2.5, "product", 1600000, "Bengaluru", "Go, Kafka, Redis"),
    ("Software Engineer", 3.0, "product", 1800000, "Gurugram", "Python, FastAPI, PostgreSQL"),
    ("Senior Software Engineer", 5.0, "product", 2500000, "Bengaluru", "Java, Kotlin, Microservices"),
    ("Senior Software Engineer", 6.0, "product", 3000000, "Bengaluru", "Python, ML, AWS"),
    ("Senior Software Engineer", 7.0, "product", 3500000, "Bengaluru", "Go, Kubernetes, GCP"),
    ("Staff Engineer", 9.0, "product", 5000000, "Bengaluru", "Distributed Systems, Java"),
    ("Staff Engineer", 10.0, "product", 5500000, "Bengaluru", "Python, ML Platform"),
    ("Product Manager", 4.0, "product", 3000000, "Bengaluru", "SQL, Analytics, PM"),
    ("Product Manager", 6.0, "product", 4000000, "Gurugram", "SQL, A/B Testing"),
    ("Senior Product Manager", 8.0, "product", 5500000, "Bengaluru", "Product Strategy"),
    ("Data Scientist", 3.0, "product", 2200000, "Bengaluru", "Python, ML, Scikit-learn"),
    ("Data Scientist", 5.0, "product", 3200000, "Bengaluru", "Python, Deep Learning, PyTorch"),
    ("ML Engineer", 4.0, "product", 2800000, "Bengaluru", "Python, TensorFlow, AWS SageMaker"),
    ("ML Engineer", 6.0, "product", 4000000, "Bengaluru", "PyTorch, Kubernetes, MLOps"),
    ("Frontend Engineer", 3.0, "product", 1800000, "Bengaluru", "React, TypeScript, GraphQL"),
    ("Frontend Engineer", 5.0, "product", 2800000, "Bengaluru", "React, Next.js, Performance"),
    ("Backend Engineer", 3.5, "product", 2200000, "Bengaluru", "Node.js, PostgreSQL, Redis"),
    ("Backend Engineer", 5.5, "product", 3200000, "Hyderabad", "Java, Kafka, AWS"),
    ("Engineering Manager", 8.0, "product", 5000000, "Bengaluru", "People Management"),
    ("Engineering Manager", 10.0, "product", 7000000, "Bengaluru", "Org Design, Delivery"),
    ("UX Designer", 3.0, "product", 1600000, "Bengaluru", "Figma, User Research"),
    ("UX Designer", 5.0, "product", 2400000, "Bengaluru", "Figma, Design Systems"),
    ("DevOps/SRE", 4.0, "product", 2500000, "Bengaluru", "AWS, Terraform, Prometheus"),
    ("SRE", 6.0, "product", 3500000, "Bengaluru", "GCP, Kubernetes, SLO"),
    # --- Startups ---
    ("Full Stack Engineer", 2.0, "startup", 1200000, "Bengaluru", "React, Node.js, MongoDB"),
    ("Full Stack Engineer", 3.0, "startup", 1600000, "Bengaluru", "Next.js, Python, PostgreSQL"),
    ("Full Stack Engineer", 4.0, "startup", 2000000, "Mumbai", "React, Go, AWS"),
    ("Backend Engineer", 2.5, "startup", 1400000, "Bengaluru", "Python, FastAPI, Redis"),
    ("Backend Engineer", 4.0, "startup", 2000000, "Bengaluru", "Go, Postgres, Kafka"),
    ("Product Manager", 3.0, "startup", 2000000, "Bengaluru", "Analytics, Product"),
    ("Product Manager", 5.0, "startup", 3000000, "Bengaluru", "0-to-1, Growth"),
    ("Data Analyst", 2.0, "startup", 1000000, "Bengaluru", "SQL, Python, Looker"),
    ("Data Analyst", 3.5, "startup", 1500000, "Bengaluru", "SQL, dbt, Metabase"),
    ("Growth Manager", 3.0, "startup", 1800000, "Bengaluru", "Performance Marketing, SQL"),
    ("Growth Manager", 5.0, "startup", 2500000, "Bengaluru", "Attribution, A/B Testing"),
    ("ML Engineer", 3.0, "startup", 2000000, "Bengaluru", "Python, Hugging Face, AWS"),
    ("Frontend Engineer", 2.5, "startup", 1200000, "Bengaluru", "React, TypeScript"),
    ("CTO / Tech Lead", 7.0, "startup", 3000000, "Bengaluru", "Architecture, Hiring"),
    # --- Unicorn / Big Tech ---
    ("Software Engineer (SDE-1)", 2.0, "unicorn", 2500000, "Bengaluru", "Java, Spring, AWS"),
    ("Software Engineer (SDE-2)", 4.0, "unicorn", 3500000, "Bengaluru", "Java, Distributed Systems"),
    ("Software Engineer (SDE-2)", 5.0, "unicorn", 4000000, "Bengaluru", "Go, Kubernetes, GCP"),
    ("Senior SDE (SDE-3)", 7.0, "unicorn", 5500000, "Bengaluru", "System Design, Java"),
    ("Senior SDE (SDE-3)", 8.0, "unicorn", 6500000, "Bengaluru", "Python, ML, AWS"),
    ("Principal Engineer", 11.0, "unicorn", 10000000, "Bengaluru", "Platform, Architecture"),
    ("Data Scientist", 3.0, "unicorn", 3000000, "Bengaluru", "Python, Spark, MLflow"),
    ("Data Scientist", 5.0, "unicorn", 4500000, "Bengaluru", "ML, Python, Hadoop"),
    ("ML Scientist", 6.0, "unicorn", 6000000, "Bengaluru", "Deep Learning, Research"),
    ("Product Manager (APM)", 2.0, "unicorn", 2200000, "Bengaluru", "SQL, Analytics"),
    ("Product Manager (PM)", 5.0, "unicorn", 5000000, "Bengaluru", "Monetization, Analytics"),
    ("Senior PM", 8.0, "unicorn", 7000000, "Gurugram", "Strategy, Data"),
    ("Director of Engineering", 12.0, "unicorn", 15000000, "Bengaluru", "Org Scale, Vision"),
    ("UX Designer", 4.0, "unicorn", 2800000, "Bengaluru", "Figma, Research, Systems"),
    ("Backend Engineer", 3.0, "unicorn", 3200000, "Hyderabad", "Java, gRPC, Kafka"),
    # More service company data
    ("Associate Consultant", 1.5, "service", 600000, "Bengaluru", "SQL, Excel"),
    ("Consultant", 3.0, "service", 1000000, "Bengaluru", "SAP, ABAP"),
    ("Senior Consultant", 5.5, "service", 1500000, "Hyderabad", "ServiceNow, ITSM"),
    ("UI Developer", 2.0, "service", 650000, "Chennai", "Angular, HTML, CSS"),
    ("Mainframe Developer", 6.0, "service", 1400000, "Pune", "COBOL, JCL, VSAM"),
    ("Network Engineer", 4.0, "service", 900000, "Bengaluru", "CCNA, Cisco, BGP"),
    ("Cybersecurity Analyst", 3.5, "service", 1100000, "Bengaluru", "SIEM, SOC, Python"),
    # More product + startup
    ("Android Engineer", 4.0, "product", 2600000, "Bengaluru", "Kotlin, Jetpack Compose"),
    ("iOS Engineer", 4.0, "product", 2600000, "Bengaluru", "Swift, SwiftUI, Xcode"),
    ("Android Engineer", 2.5, "startup", 1300000, "Bengaluru", "Kotlin, XML"),
    ("iOS Engineer", 3.0, "startup", 1500000, "Mumbai", "Swift, Objective-C"),
    ("Data Engineer", 4.0, "product", 2800000, "Bengaluru", "Spark, Airflow, dbt"),
    ("Data Engineer", 3.0, "startup", 1800000, "Bengaluru", "Python, dbt, Snowflake"),
    ("Platform Engineer", 5.0, "product", 3200000, "Bengaluru", "Terraform, AWS, Python"),
    ("Security Engineer", 5.0, "unicorn", 4500000, "Bengaluru", "AppSec, SAST, Pentesting"),
    ("Business Intelligence", 3.0, "product", 1800000, "Gurugram", "SQL, Tableau, Looker"),
    ("Technical Program Manager", 7.0, "product", 4000000, "Bengaluru", "Program Mgmt, Jira"),
    ("Solution Architect", 9.0, "service", 2800000, "Bengaluru", "AWS, Azure, Solutions"),
    ("Scrum Master", 5.0, "service", 1400000, "Pune", "Agile, Jira, Confluence"),
    ("Digital Marketing Lead", 4.0, "startup", 1400000, "Bengaluru", "SEO, SEM, Analytics"),
    ("Content Strategist", 3.0, "startup", 900000, "Bengaluru", "SEO, Writing, Analytics"),
    ("HR Business Partner", 6.0, "product", 2200000, "Bengaluru", "HRBP, Performance Mgmt"),
    ("Finance Analyst", 3.0, "product", 1500000, "Mumbai", "FP&A, SQL, Excel"),
    ("Finance Analyst", 2.0, "service", 700000, "Chennai", "Excel, SAP, IFRS"),
    ("Customer Success", 3.0, "startup", 1200000, "Bengaluru", "CRM, Account Mgmt"),
    ("Technical Writer", 3.0, "product", 1300000, "Bengaluru", "API Docs, Markdown"),
    ("QA Automation Engineer", 4.0, "unicorn", 2200000, "Bengaluru", "Selenium, Python, CI/CD"),
    ("SAP Consultant", 8.0, "service", 2200000, "Hyderabad", "SAP FICO, ABAP"),
    ("Salesforce Developer", 4.0, "service", 1300000, "Chennai", "Salesforce, Apex, LWC"),
]


def seed():
    existing = SalarySubmission.objects.count()
    if existing >= 50:
        print(f"Database already has {existing} submissions. Skipping seed to avoid duplication.")
        print("Delete existing entries manually if you want to re-seed.")
        return

    created = 0
    for row in SEED_DATA:
        role, exp, company_type, ctc, city, tech_stack = row
        SalarySubmission.objects.get_or_create(
            role=role,
            experience_years=exp,
            company_type=company_type,
            ctc=ctc,
            city=city,
            defaults={
                "tech_stack": tech_stack,
                "is_verified": True,
            },
        )
        created += 1

    print(f"✓ Seeded {created} salary data points.")
    print(f"  Total in DB: {SalarySubmission.objects.count()}")


if __name__ == "__main__":
    seed()
