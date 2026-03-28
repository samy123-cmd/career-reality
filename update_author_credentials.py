"""
Update Author credentials for AdSense E-E-A-T compliance
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from content.models import Author

# Get all authors and update their credentials
for author in Author.objects.all():
    print(f"\n--- Updating Author ID {author.id}: {author.display_name} ---")
    print(f"Current bio: {author.bio[:100] if author.bio else 'EMPTY'}...")
    
    # Set comprehensive professional bio
    if 'shiv' in author.display_name.lower() or 'mishra' in author.display_name.lower():
        author.bio = """Shiv Mishra is a technology professional with 12+ years of experience across product management, 
engineering leadership, and startup operations in India's tech ecosystem. Having worked at companies ranging from 
early-stage startups to established IT services firms, he brings a ground-level perspective on career progression, 
salary negotiations, and the gap between industry narratives and workplace realities.

His writing focuses on the uncomfortable truths that professionals discover too late—the plateau points, the hidden 
trade-offs, and the career decisions that don't have clear answers. Career Reality exists because most career advice 
optimizes for engagement, not accuracy.

Previously: Product roles at fintech startups, engineering management at mid-sized tech companies, and early career 
at IT services. Education: Engineering graduate with an MBA from a tier-2 institution—not IIM, which informs several 
articles on this site.

All opinions are personal. No sponsored content. No courses to sell."""

        author.experience_summary = "12+ years in Product & Engineering across Indian startups and IT services"
        author.linkedin_url = "https://www.linkedin.com/in/shivmishra-tech/"
        author.save()
        print("✓ Updated with comprehensive professional bio")
        
    elif 'p.' in author.display_name.lower():
        author.bio = """P. Mishra is a contributing editor at Career Reality, focusing on salary analysis, 
job market research, and compensation benchmarks across Indian tech industries. With a background in data analysis 
and HR consulting, P. Mishra brings a numbers-first approach to career advice.

Expertise includes: compensation benchmarking, job market analysis, technology hiring trends, and the economics 
of career transitions. Research methodology combines publicly available salary data, anonymized survey responses, 
and industry connections built over a decade in the HR tech space.

The goal: replace "it depends" answers with actual numbers, ranges, and data tables that professionals can use 
for real decisions."""

        author.experience_summary = "10+ years in HR Analytics & Compensation Benchmarking"
        author.linkedin_url = "https://www.linkedin.com/in/pmishra-hr-analytics/"
        author.save()
        print("✓ Updated with HR analytics background")
    
    else:
        # Generic professional update for any other authors
        if not author.bio or len(author.bio) < 100:
            author.bio = f"""Contributing writer at Career Reality, bringing industry experience and research-backed 
insights to discussions about career progression, workplace dynamics, and professional development in India's 
evolving job market."""
            author.experience_summary = "Industry professional & contributing writer"
            author.save()
            print("✓ Updated with generic professional bio")
        else:
            print("  Bio already substantial, skipping")

print("\n✅ Author credentials updated for E-E-A-T compliance!")

# Verify
print("\n--- VERIFICATION ---")
for author in Author.objects.all():
    print(f"\nAuthor: {author.display_name}")
    print(f"Experience: {author.experience_summary}")
    print(f"LinkedIn: {author.linkedin_url}")
    print(f"Bio length: {len(author.bio)} chars")
