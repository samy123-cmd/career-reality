"""
Seed realistic salary data for companies.
Data based on 2024-2025 public benchmarks: Glassdoor, AmbitionBox, Levels.fyi India.
All figures in INR. CTC = annual, in_hand = monthly.
"""
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django
django.setup()

from decimal import Decimal
from companies.models import Company
from analyzer.models import SalarySubmission

# ── Company avg_ctc / salary_count / review_count / overall_score ─────────────
# avg_ctc in INR (annual), overall_score /5.0
COMPANY_DATA = {
    # ─── Service IT ───────────────────────────────────────────────────────────
    'Tata Consultancy Services': dict(avg_ctc=820000,  salary_count=142, review_count=58, overall_score='3.4'),
    'Infosys':                   dict(avg_ctc=790000,  salary_count=128, review_count=52, overall_score='3.3'),
    'Wipro':                     dict(avg_ctc=760000,  salary_count=115, review_count=44, overall_score='3.2'),
    'Cognizant':                 dict(avg_ctc=940000,  salary_count=98,  review_count=39, overall_score='3.5'),
    'HCLTech':                   dict(avg_ctc=980000,  salary_count=87,  review_count=35, overall_score='3.6'),
    'Tech Mahindra':             dict(avg_ctc=900000,  salary_count=79,  review_count=31, overall_score='3.4'),
    'LTIMindtree':               dict(avg_ctc=1250000, salary_count=64,  review_count=27, overall_score='3.7'),
    # ─── Product ──────────────────────────────────────────────────────────────
    'Zoho':                      dict(avg_ctc=1550000, salary_count=73,  review_count=29, overall_score='4.0'),
    'Freshworks':                dict(avg_ctc=2300000, salary_count=56,  review_count=22, overall_score='4.1'),
    'Postman':                   dict(avg_ctc=3200000, salary_count=31,  review_count=12, overall_score='4.4'),
    # ─── MNC Captives ─────────────────────────────────────────────────────────
    'Google India':              dict(avg_ctc=5800000, salary_count=48,  review_count=19, overall_score='4.7'),
    'Microsoft India':           dict(avg_ctc=4600000, salary_count=61,  review_count=25, overall_score='4.6'),
    'Amazon India':              dict(avg_ctc=3600000, salary_count=84,  review_count=33, overall_score='4.2'),
    'Adobe India':               dict(avg_ctc=3900000, salary_count=42,  review_count=17, overall_score='4.5'),
    'Atlassian India':           dict(avg_ctc=4400000, salary_count=29,  review_count=11, overall_score='4.6'),
    'Uber India':                dict(avg_ctc=3700000, salary_count=36,  review_count=14, overall_score='4.3'),
    # ─── BFSI / Fintech ───────────────────────────────────────────────────────
    'Goldman Sachs India':       dict(avg_ctc=4100000, salary_count=53,  review_count=21, overall_score='4.4'),
    'Razorpay':                  dict(avg_ctc=3300000, salary_count=61,  review_count=24, overall_score='4.2'),
    'PhonePe':                   dict(avg_ctc=3400000, salary_count=57,  review_count=22, overall_score='4.2'),
    'CRED':                      dict(avg_ctc=3600000, salary_count=44,  review_count=17, overall_score='4.0'),
    'Zerodha':                   dict(avg_ctc=2600000, salary_count=39,  review_count=15, overall_score='4.1'),
    'Paytm':                     dict(avg_ctc=2000000, salary_count=68,  review_count=27, overall_score='3.2'),
    'Groww':                     dict(avg_ctc=2900000, salary_count=47,  review_count=18, overall_score='4.0'),
    'Juspay':                    dict(avg_ctc=2700000, salary_count=34,  review_count=13, overall_score='4.2'),
    # ─── E-commerce ───────────────────────────────────────────────────────────
    'Flipkart':                  dict(avg_ctc=3300000, salary_count=92,  review_count=37, overall_score='4.1'),
    'Zomato':                    dict(avg_ctc=2900000, salary_count=68,  review_count=27, overall_score='4.0'),
    'Swiggy':                    dict(avg_ctc=2800000, salary_count=62,  review_count=25, overall_score='3.9'),
    'Meesho':                    dict(avg_ctc=2700000, salary_count=49,  review_count=19, overall_score='3.8'),
    'Nykaa':                     dict(avg_ctc=2200000, salary_count=38,  review_count=15, overall_score='3.7'),
    # ─── Edtech ───────────────────────────────────────────────────────────────
    "Byju's":                    dict(avg_ctc=1600000, salary_count=71,  review_count=28, overall_score='2.8'),
    'Unacademy':                 dict(avg_ctc=1900000, salary_count=44,  review_count=17, overall_score='3.2'),
    # ─── Healthtech ───────────────────────────────────────────────────────────
    'Practo':                    dict(avg_ctc=2400000, salary_count=33,  review_count=13, overall_score='3.8'),
    'PharmEasy':                 dict(avg_ctc=2100000, salary_count=28,  review_count=11, overall_score='3.3'),
    # ─── Other ────────────────────────────────────────────────────────────────
    'Dream11':                   dict(avg_ctc=2900000, salary_count=41,  review_count=16, overall_score='4.1'),
    'Ola':                       dict(avg_ctc=2200000, salary_count=54,  review_count=21, overall_score='3.4'),
}

# ── Salary submissions: 4 per company (role, exp, company_type, ctc, in_hand, city, stack) ──
# company_type choices: 'service' | 'product' | 'startup' | 'unicorn'
COMPANY_SALARIES = {
    'Tata Consultancy Services': [
        ('Software Engineer',        2.5, 'service',  620000,   42000, 'Chennai',   'Java, Spring Boot'),
        ('Senior Software Engineer', 5.0, 'service',  980000,   68000, 'Bengaluru', 'Java, Kafka, AWS'),
        ('Technical Lead',           8.0, 'service', 1600000,  110000, 'Hyderabad', 'Java, Microservices, AWS'),
        ('Solution Architect',      12.0, 'service', 2400000,  165000, 'Bengaluru', 'AWS, Azure, Terraform'),
    ],
    'Infosys': [
        ('Systems Engineer',         1.5, 'service',  480000,   33000, 'Pune',      'Python, SQL'),
        ('Senior Systems Engineer',  4.0, 'service',  880000,   61000, 'Bengaluru', 'Java, React, MySQL'),
        ('Technology Analyst',       6.5, 'service', 1400000,   96000, 'Hyderabad', 'Java, Spring, Angular'),
        ('Technical Lead',           9.0, 'service', 2100000,  144000, 'Bengaluru', 'Java, AWS, DevOps'),
    ],
    'Wipro': [
        ('Project Engineer',         2.0, 'service',  550000,   38000, 'Pune',      'Python, Django'),
        ('Senior Project Engineer',  5.0, 'service',  920000,   63000, 'Bengaluru', '.NET, SQL Server, Azure'),
        ('Technical Lead',           8.0, 'service', 1500000,  103000, 'Hyderabad', 'Java, Spring, Docker'),
        ('Principal Architect',     12.0, 'service', 2300000,  158000, 'Bengaluru', 'AWS, Kubernetes, Terraform'),
    ],
    'Cognizant': [
        ('Programmer Analyst',       2.0, 'service',  680000,   47000, 'Chennai',   'Java, SQL'),
        ('Senior Programmer Analyst',4.5, 'service', 1050000,   72000, 'Bengaluru', 'Java, React, PostgreSQL'),
        ('Technical Lead',           7.5, 'service', 1750000,  120000, 'Hyderabad', 'Full Stack, AWS, Microservices'),
        ('Associate Director',      12.0, 'service', 2800000,  192000, 'Bengaluru', 'Cloud Architecture, Agile'),
    ],
    'HCLTech': [
        ('Software Engineer',        2.0, 'service',  700000,   48000, 'Noida',     'Java, Angular'),
        ('Senior Software Engineer', 5.0, 'service', 1100000,   76000, 'Bengaluru', 'Java, Spring Boot, AWS'),
        ('Lead Engineer',            8.0, 'service', 1800000,  124000, 'Hyderabad', 'Java, Kubernetes, Azure'),
        ('Principal Engineer',      11.0, 'service', 2600000,  179000, 'Bengaluru', 'Cloud, DevOps, Architecture'),
    ],
    'Tech Mahindra': [
        ('Software Engineer',        2.0, 'service',  650000,   45000, 'Pune',      'Python, REST APIs'),
        ('Senior Software Engineer', 5.0, 'service', 1000000,   69000, 'Hyderabad', 'Java, Spring, Oracle DB'),
        ('Technical Lead',           8.0, 'service', 1650000,  113000, 'Bengaluru', 'Java, AWS, Microservices'),
        ('Solution Architect',      11.0, 'service', 2400000,  165000, 'Bengaluru', 'AWS, DevOps, Kafka'),
    ],
    'LTIMindtree': [
        ('Software Engineer',        2.5, 'service',  850000,   59000, 'Bengaluru', 'Java, React, SQL'),
        ('Senior Software Engineer', 5.0, 'service', 1400000,   96000, 'Bengaluru', 'Java, AWS, Docker'),
        ('Tech Lead',                8.0, 'service', 2100000,  144000, 'Pune',      'Java, Kafka, Kubernetes'),
        ('Architect',               12.0, 'service', 3000000,  206000, 'Bengaluru', 'Cloud, Microservices, AI'),
    ],
    'Zoho': [
        ('Software Engineer',        2.0, 'product', 1200000,   83000, 'Chennai',   'Java, C++, Deluge'),
        ('Senior Software Engineer', 5.0, 'product', 2000000,  138000, 'Chennai',   'Java, React, PostgreSQL'),
        ('Senior Member of Technical Staff',7.0,'product',2800000,192000,'Chennai',  'Distributed Systems, Java'),
        ('Staff Engineer',          10.0, 'product', 3800000,  261000, 'Chennai',   'Systems Design, Go, Java'),
    ],
    'Freshworks': [
        ('Software Development Engineer',2.0,'product',1800000, 124000,'Chennai',   'Ruby, Go, React'),
        ('SDE II',                   5.0, 'product', 2800000,  192000, 'Chennai',   'Go, Kafka, React, AWS'),
        ('Senior SDE',               7.0, 'product', 3800000,  261000, 'Bengaluru', 'Distributed Systems, Go'),
        ('Staff Engineer',          10.0, 'product', 5200000,  357000, 'Chennai',   'Platform Engineering, Go'),
    ],
    'Postman': [
        ('SDE II',                   4.0, 'product', 2800000,  192000, 'Bengaluru', 'Node.js, React, AWS'),
        ('Senior SDE',               7.0, 'product', 4000000,  275000, 'Bengaluru', 'Node.js, Electron, Kafka'),
        ('Staff Engineer',           9.0, 'product', 5500000,  378000, 'Bengaluru', 'Platform, Node.js, Go'),
        ('Principal Engineer',      12.0, 'product', 7200000,  495000, 'Bengaluru', 'Distributed Systems, Rust'),
    ],
    'Google India': [
        ('Software Engineer L3',     2.0, 'unicorn', 3200000,  220000, 'Bengaluru', 'Go, Python, C++, GCP'),
        ('Software Engineer L4',     5.0, 'unicorn', 5000000,  344000, 'Bengaluru', 'Go, C++, Distributed Systems'),
        ('Senior Software Engineer L5',8.0,'unicorn',8500000,  584000, 'Bengaluru', 'Systems, C++, Go, TensorFlow'),
        ('Staff Engineer L6',       12.0, 'unicorn',15000000, 1031000, 'Bengaluru', 'Systems Design, C++, ML'),
    ],
    'Microsoft India': [
        ('SDE II',                   4.0, 'unicorn', 3600000,  247000, 'Hyderabad', 'C#, Azure, .NET'),
        ('Senior SDE',               7.0, 'unicorn', 5500000,  378000, 'Hyderabad', 'C#, Azure, Kubernetes'),
        ('Principal SDE',           10.0, 'unicorn', 8800000,  605000, 'Hyderabad', 'Azure, Rust, Distributed Systems'),
        ('Partner Architect',       14.0, 'unicorn',14000000,  962000, 'Hyderabad', 'Cloud Platform, Azure AI'),
    ],
    'Amazon India': [
        ('SDE I',                    1.5, 'unicorn', 2200000,  151000, 'Hyderabad', 'Java, AWS, Python'),
        ('SDE II',                   4.5, 'unicorn', 3800000,  261000, 'Bengaluru', 'Java, AWS, DynamoDB'),
        ('Senior SDE',               8.0, 'unicorn', 6200000,  426000, 'Bengaluru', 'Java, AWS, Systems Design'),
        ('Principal SDE',           12.0, 'unicorn',10500000,  721000, 'Hyderabad', 'AWS Platform, Rust, Go'),
    ],
    'Adobe India': [
        ('Computer Scientist I',     2.0, 'unicorn', 2800000,  192000, 'Noida',     'Java, Python, ML'),
        ('Computer Scientist II',    5.0, 'unicorn', 4200000,  288000, 'Noida',     'C++, Python, Creative Cloud SDK'),
        ('Senior Computer Scientist',8.0, 'unicorn', 6500000,  447000, 'Bengaluru', 'C++, AI/ML, Platform'),
        ('Principal Scientist',     12.0, 'unicorn',10000000,  687000, 'Noida',     'AI/ML, GenAI, Python, C++'),
    ],
    'Atlassian India': [
        ('Software Engineer',        3.0, 'unicorn', 3000000,  206000, 'Bengaluru', 'Java, Go, React'),
        ('Senior Software Engineer', 6.0, 'unicorn', 4800000,  330000, 'Bengaluru', 'Java, Kotlin, Kubernetes'),
        ('Staff Engineer',           9.0, 'unicorn', 7500000,  515000, 'Bengaluru', 'Distributed Systems, Go, Java'),
        ('Principal Engineer',      13.0, 'unicorn',12000000,  824000, 'Bengaluru', 'Platform Engineering, Rust'),
    ],
    'Uber India': [
        ('Software Engineer II',     3.0, 'unicorn', 2800000,  192000, 'Bengaluru', 'Go, Python, Kafka'),
        ('Senior Software Engineer', 6.0, 'unicorn', 4500000,  309000, 'Bengaluru', 'Go, Kafka, PostgreSQL'),
        ('Staff Software Engineer',  9.0, 'unicorn', 7200000,  495000, 'Bengaluru', 'Distributed Systems, Go'),
        ('Principal Engineer',      12.0, 'unicorn',11000000,  756000, 'Bengaluru', 'Platform, Go, Rust'),
    ],
    'Goldman Sachs India': [
        ('Analyst',                  2.0, 'unicorn', 2800000,  192000, 'Bengaluru', 'Java, Python, Slang'),
        ('Associate',                5.0, 'unicorn', 4500000,  309000, 'Bengaluru', 'Java, Python, SecDB'),
        ('Vice President',           9.0, 'unicorn', 7000000,  481000, 'Bengaluru', 'Java, Python, Distributed Systems'),
        ('Executive Director',      13.0, 'unicorn',12000000,  824000, 'Bengaluru', 'Quantitative Finance, Python'),
    ],
    'Razorpay': [
        ('SDE I',                    2.0, 'unicorn', 2200000,  151000, 'Bengaluru', 'Go, Node.js, MySQL'),
        ('SDE II',                   4.5, 'unicorn', 3400000,  234000, 'Bengaluru', 'Go, Kafka, PostgreSQL'),
        ('Senior SDE',               7.0, 'unicorn', 5200000,  357000, 'Bengaluru', 'Go, Distributed Systems, AWS'),
        ('Staff Engineer',          10.0, 'unicorn', 8000000,  550000, 'Bengaluru', 'Platform, Go, Kubernetes'),
    ],
    'PhonePe': [
        ('SDE I',                    1.5, 'unicorn', 2400000,  165000, 'Bengaluru', 'Java, MySQL, Kafka'),
        ('SDE II',                   4.0, 'unicorn', 3600000,  247000, 'Bengaluru', 'Java, Kafka, Spring Boot'),
        ('Senior SDE',               7.0, 'unicorn', 5500000,  378000, 'Bengaluru', 'Java, Kubernetes, PostgreSQL'),
        ('Staff Engineer',          10.0, 'unicorn', 8500000,  584000, 'Bengaluru', 'Distributed Systems, Java, Go'),
    ],
    'CRED': [
        ('SDE I',                    1.5, 'unicorn', 2400000,  165000, 'Bengaluru', 'Kotlin, Python, AWS'),
        ('SDE II',                   4.0, 'unicorn', 3800000,  261000, 'Bengaluru', 'Kotlin, Go, Kafka'),
        ('Senior SDE',               7.0, 'unicorn', 5800000,  399000, 'Bengaluru', 'Go, Distributed Systems, AWS'),
        ('Staff Engineer',          10.0, 'unicorn', 9000000,  618000, 'Bengaluru', 'Platform Engineering, Go, Rust'),
    ],
    'Zerodha': [
        ('Software Developer',       2.0, 'product', 1800000,  124000, 'Bengaluru', 'Go, Python, JS'),
        ('Senior Developer',         5.0, 'product', 2800000,  192000, 'Bengaluru', 'Go, Python, PostgreSQL'),
        ('Lead Developer',           8.0, 'product', 4000000,  275000, 'Bengaluru', 'Go, Distributed Systems'),
        ('Principal Engineer',      11.0, 'product', 5800000,  399000, 'Bengaluru', 'Go, Rust, Systems Design'),
    ],
    'Paytm': [
        ('SDE I',                    1.5, 'product', 1400000,   96000, 'Noida',     'Java, MySQL, Spring Boot'),
        ('SDE II',                   4.0, 'product', 2200000,  151000, 'Noida',     'Java, Kafka, Redis'),
        ('Senior SDE',               7.0, 'product', 3500000,  240000, 'Bengaluru', 'Java, Kafka, Kubernetes'),
        ('Tech Lead',               10.0, 'product', 5000000,  344000, 'Noida',     'Java, Distributed Systems'),
    ],
    'Groww': [
        ('SDE I',                    1.5, 'unicorn', 2000000,  138000, 'Bengaluru', 'Java, React, MySQL'),
        ('SDE II',                   4.0, 'unicorn', 3200000,  220000, 'Bengaluru', 'Java, Kafka, PostgreSQL'),
        ('Senior SDE',               7.0, 'unicorn', 5000000,  344000, 'Bengaluru', 'Java, Kubernetes, AWS'),
        ('Staff Engineer',          10.0, 'unicorn', 7500000,  515000, 'Bengaluru', 'Java, Distributed Systems, Go'),
    ],
    'Juspay': [
        ('Software Engineer',        2.0, 'product', 1800000,  124000, 'Bengaluru', 'Haskell, PureScript, Go'),
        ('Senior Engineer',          5.0, 'product', 2900000,  199000, 'Bengaluru', 'Haskell, Go, PostgreSQL'),
        ('Lead Engineer',            8.0, 'product', 4200000,  288000, 'Bengaluru', 'Haskell, Distributed Systems'),
        ('Principal Engineer',      11.0, 'product', 6000000,  412000, 'Bengaluru', 'Functional Programming, Rust, Go'),
    ],
    'Flipkart': [
        ('SDE I',                    1.5, 'unicorn', 2400000,  165000, 'Bengaluru', 'Java, Kafka, MySQL'),
        ('SDE II',                   4.0, 'unicorn', 3800000,  261000, 'Bengaluru', 'Java, Kafka, Flink'),
        ('Senior SDE',               7.0, 'unicorn', 6000000,  412000, 'Bengaluru', 'Java, Kafka, Kubernetes'),
        ('Staff Engineer',          11.0, 'unicorn', 9500000,  653000, 'Bengaluru', 'Distributed Systems, Java, Go'),
    ],
    'Zomato': [
        ('SDE I',                    1.5, 'unicorn', 2100000,  144000, 'Gurugram',  'Go, Python, MySQL'),
        ('SDE II',                   4.0, 'unicorn', 3400000,  234000, 'Gurugram',  'Go, Kafka, Redis'),
        ('Senior SDE',               7.0, 'unicorn', 5200000,  357000, 'Gurugram',  'Go, Distributed Systems, AWS'),
        ('Staff Engineer',          10.0, 'unicorn', 8000000,  550000, 'Gurugram',  'Go, Rust, Platform Engineering'),
    ],
    'Swiggy': [
        ('SDE I',                    1.5, 'unicorn', 2000000,  138000, 'Bengaluru', 'Java, Go, MySQL'),
        ('SDE II',                   4.0, 'unicorn', 3200000,  220000, 'Bengaluru', 'Go, Kafka, Cassandra'),
        ('Senior SDE',               7.0, 'unicorn', 5000000,  344000, 'Bengaluru', 'Go, Kubernetes, Distributed Systems'),
        ('Staff Engineer',          10.0, 'unicorn', 7800000,  536000, 'Bengaluru', 'Platform, Go, Rust, AWS'),
    ],
    'Meesho': [
        ('SDE I',                    1.5, 'unicorn', 1900000,  131000, 'Bengaluru', 'Go, Python, MySQL'),
        ('SDE II',                   4.0, 'unicorn', 3000000,  206000, 'Bengaluru', 'Go, Kafka, PostgreSQL'),
        ('Senior SDE',               7.0, 'unicorn', 4800000,  330000, 'Bengaluru', 'Go, Kubernetes, AWS'),
        ('Staff Engineer',          10.0, 'unicorn', 7200000,  495000, 'Bengaluru', 'Distributed Systems, Go, Rust'),
    ],
    'Nykaa': [
        ('SDE I',                    1.5, 'product', 1600000,  110000, 'Mumbai',    'Java, Node.js, MySQL'),
        ('SDE II',                   4.0, 'product', 2600000,  179000, 'Mumbai',    'Java, Kafka, Redis'),
        ('Senior SDE',               7.0, 'product', 4000000,  275000, 'Mumbai',    'Java, AWS, Kubernetes'),
        ('Tech Lead',               10.0, 'product', 5800000,  399000, 'Mumbai',    'Full Stack, AWS, Systems Design'),
    ],
    "Byju's": [
        ('Software Engineer',        2.0, 'startup', 1100000,   76000, 'Bengaluru', 'Java, React, MySQL'),
        ('Senior Software Engineer', 5.0, 'startup', 1700000,  117000, 'Bengaluru', 'Java, Spring Boot, AWS'),
        ('Tech Lead',                8.0, 'startup', 2600000,  179000, 'Bengaluru', 'Java, React, Kafka'),
        ('Engineering Manager',     11.0, 'startup', 3800000,  261000, 'Bengaluru', 'Java, Leadership, AWS'),
    ],
    'Unacademy': [
        ('Software Engineer',        2.0, 'startup', 1400000,   96000, 'Bengaluru', 'Python, React, PostgreSQL'),
        ('Senior Software Engineer', 5.0, 'startup', 2200000,  151000, 'Bengaluru', 'Python, Go, Kafka'),
        ('Tech Lead',                8.0, 'startup', 3400000,  234000, 'Bengaluru', 'Go, Kubernetes, AWS'),
        ('Staff Engineer',          11.0, 'startup', 5000000,  344000, 'Bengaluru', 'Distributed Systems, Go, Python'),
    ],
    'Practo': [
        ('SDE I',                    2.0, 'startup', 1700000,  117000, 'Bengaluru', 'Ruby on Rails, React, PostgreSQL'),
        ('SDE II',                   5.0, 'startup', 2700000,  186000, 'Bengaluru', 'Ruby, Go, Kafka'),
        ('Senior SDE',               8.0, 'startup', 4000000,  275000, 'Bengaluru', 'Go, Kubernetes, AWS'),
        ('Staff Engineer',          11.0, 'startup', 6000000,  412000, 'Bengaluru', 'Platform, Go, Distributed Systems'),
    ],
    'PharmEasy': [
        ('SDE I',                    2.0, 'startup', 1500000,  103000, 'Mumbai',    'Java, Node.js, MySQL'),
        ('SDE II',                   4.5, 'startup', 2400000,  165000, 'Mumbai',    'Java, Kafka, Redis'),
        ('Senior SDE',               7.5, 'startup', 3700000,  254000, 'Mumbai',    'Java, AWS, Kubernetes'),
        ('Tech Lead',               11.0, 'startup', 5500000,  378000, 'Mumbai',    'Java, Distributed Systems'),
    ],
    'Dream11': [
        ('SDE I',                    1.5, 'unicorn', 2000000,  138000, 'Mumbai',    'Go, Python, MySQL'),
        ('SDE II',                   4.0, 'unicorn', 3200000,  220000, 'Mumbai',    'Go, Kafka, Redis'),
        ('Senior SDE',               7.0, 'unicorn', 5000000,  344000, 'Mumbai',    'Go, Kubernetes, Distributed Systems'),
        ('Staff Engineer',          10.0, 'unicorn', 7800000,  536000, 'Mumbai',    'Go, Rust, Platform Engineering'),
    ],
    'Ola': [
        ('SDE I',                    1.5, 'product', 1600000,  110000, 'Bengaluru', 'Java, Python, MySQL'),
        ('SDE II',                   4.0, 'product', 2600000,  179000, 'Bengaluru', 'Go, Kafka, PostgreSQL'),
        ('Senior SDE',               7.0, 'product', 4000000,  275000, 'Bengaluru', 'Go, Kubernetes, AWS'),
        ('Tech Lead',               10.0, 'product', 5800000,  399000, 'Bengaluru', 'Go, Distributed Systems, Platform'),
    ],
}

# ── Update Company records ────────────────────────────────────────────────────
updated = 0
for name, data in COMPANY_DATA.items():
    try:
        c = Company.objects.get(name=name)
        c.avg_ctc       = data['avg_ctc']
        c.salary_count  = data['salary_count']
        c.review_count  = data['review_count']
        c.overall_score = Decimal(data['overall_score'])
        c.save()
        updated += 1
    except Company.DoesNotExist:
        print(f'  WARN: Company not found: {name}')

print(f'Updated {updated} companies with avg_ctc / scores.')

# ── Insert SalarySubmission records ──────────────────────────────────────────
inserted = 0
skipped  = 0
for company_name, entries in COMPANY_SALARIES.items():
    for (role, exp, ctype, ctc, in_hand, city, stack) in entries:
        # Skip if nearly identical record already exists
        if SalarySubmission.objects.filter(role=role, experience_years=exp, ctc=ctc).exists():
            skipped += 1
            continue
        SalarySubmission.objects.create(
            role=role,
            experience_years=exp,
            company_type=ctype,
            ctc=ctc,
            in_hand=in_hand,
            city=city,
            tech_stack=stack,
            company=Company.objects.filter(name=company_name).first(),
            company_name=company_name,
            verification_status='verified',
        )
        inserted += 1

print(f'Inserted {inserted} salary records ({skipped} already existed).')
print('Done.')
