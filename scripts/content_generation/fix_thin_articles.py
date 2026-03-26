"""Fix remaining THIN/CRITICAL articles with more comprehensive content"""
import os
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from content.models import Article

# These articles need more sections filled out
expansions = {
    4: {  # Digital Marketing - needs common_expectation and stuck_point
        "common_expectation": """<p>Digital marketing is sold as the creative career path. "Tell brand stories." "Create viral campaigns." "Work with influencers." Course ads show people working on laptops in cafes, making six figures while being creative.</p>

<p>The expectation: You'll spend your days crafting compelling narratives, shooting content, and watching your campaigns go viral. It's marketing meets art, with good money thrown in.</p>

<p>Who wouldn't want to be paid to be creative?</p>""",
        
        "stuck_point": """<p><strong>Where Digital Marketers Get Trapped:</strong></p>

<p><strong>The Platform Dependency Trap:</strong></p>
<p>Your entire career depends on Facebook, Google, and Instagram algorithms. When they change (every 6 months), your expertise resets. When they ban your ad account (happens arbitrarily), your client loses their month. You're at the mercy of platforms you don't control.</p>

<p><strong>The Agency Burnout Spiral:</strong></p>
<p>Agency work teaches fast but burns faster. 12 clients, 60-hour weeks, constant fire-drills. By month 18, you're exhausted. You move to in-house, get bored, miss the variety. Return to agency, burn out again. The cycle repeats.</p>

<p><strong>The "Not Quite Business" Problem:</strong></p>
<p>Marketing sits between creative and business. You're not technical enough for product, not analytical enough for finance, not strategic enough for consulting. When companies cut costs, marketing goes early because it's seen as "cost center."</p>

<p><strong>Escape Routes That Work:</strong></p>

<ol>
<li><strong>Specialize in High-Impact Areas</strong>: SEO, CRO (conversion rate optimization), marketing automation. These require deeper skills that are harder to commoditize.</li>

<li><strong>Build Data Skills</strong>: SQL, marketing analytics, attribution modeling. The marketers who can prove ROI command premiums.</li>

<li><strong>Move to Product Marketing</strong>: Bridge role between marketing and product. Better pay, more strategic work, clearer career path.</li>

<li><strong>Consider Growth Roles</strong>: Growth marketing/growth product combines marketing with product thinking. More technical, better paid.</li>

<li><strong>Consulting Exit</strong>: After 10+ years, independent consulting pays Rs 5-15K/hour. But only for specialists with proven track records.</li>
</ol>""",
    },
    
    16: {  # Upskilling - needs common_expectation
        "common_expectation": """<p>Every LinkedIn influencer tells you to upskill. "Learn Python." "Get AWS certified." "Master AI." The message is clear: in a fast-changing world, your skills are your security. Those who upskill win; those who don't fall behind.</p>

<p>The expectation: Continuously learning new skills will continuously increase your value. Each new certification, each new technology mastered, compounds into career success.</p>

<p>The learning never stops—that's the deal.</p>""",
    },
    
    17: {  # IT Services - needs common_expectation
        "common_expectation": """<p>IT services companies (TCS, Infosys, Wipro, HCL) are the entry point for lakhs of Indian engineers each year. "Good training ground." "Learn enterprise development." "Stable career." Parents approve, placement cells celebrate.</p>

<p>The expectation: Start here, learn the ropes, then move to better opportunities. It's a stepping stone, not a destination. Everyone knows you shouldn't stay long, but the exact timeline is fuzzy.</p>

<p>How long is too long? When does the stepping stone become a trap?</p>""",
    },
    
    18: {  # Career Switching - needs common_expectation
        "common_expectation": """<p>Career switching stories are everywhere. "I left banking for UX design and never looked back." "Went from teaching to tech and doubled my salary." LinkedIn celebrates the pivot. It seems like with enough courage and hustle, anyone can reinvent themselves.</p>

<p>The expectation: If you're unhappy or stuck, switch careers. Your current skills will transfer. Your experience will be valued. Within a year or two, you'll be thriving in your new path.</p>

<p>The stories make it look achievable. Is it?</p>""",
    },
    
    19: {  # Data Science - needs common_expectation
        "common_expectation": """<p>Data Science is the "sexiest job of the 21st century." Every course promises: Learn Python and ML, become a Data Scientist, earn Rs 15-30 LPA. The career pages show people building AI models, presenting insights to C-suite, changing business strategy with data.</p>

<p>The expectation: Apply machine learning to real problems. Build recommendation engines. Create predictive models. Work at the cutting edge of technology and business.</p>

<p>Kaggle competitions, neural networks, research papers—that's the Data Science dream.</p>""",
    },
    
    20: {  # Frontend - needs common_expectation
        "common_expectation": """<p>Frontend development seems like the accessible path into tech. "Learn React, get a job." Bootcamps promise job-readiness in 3-6 months. Unlike backend, you can see what you build immediately. Unlike DevOps, the learning curve seems gentler.</p>

<p>The expectation: Master React (or Vue, or Angular), land a job, and you're set. Frontend developers are in demand. The skills are portable. The work is creative.</p>

<p>It's the developer role that doesn't require a CS degree—or so they say.</p>""",
    },
    
    21: {  # PM - needs common_expectation
        "common_expectation": """<p>"The PM is the CEO of the product." This phrase, from a famous essay, defined how a generation thinks about product management. The PM sets vision, makes decisions, leads without authority. It's the role for people who want business impact without coding.</p>

<p>The expectation: Spend your days thinking about strategy, talking to users, prioritizing features based on data and insight. You're the one who decides what gets built. You're the voice of the customer.</p>

<p>MBA graduates flood into PM roles chasing this vision.</p>""",
    },
    
    22: {  # Agency vs Brand - needs common_expectation
        "common_expectation": """<p>The marketing world is split: agency side and brand side. Agency is where the action is—multiple clients, creative campaigns, fast-paced environment. Brand side is the promised land—better hours, deeper work, one brand to focus on.</p>

<p>The expectation: Start agency for experience, move brand-side for lifestyle. Each has trade-offs, but the path is clear. You can switch between them as your priorities change.</p>

<p>Sounds like the best of both worlds is achievable.</p>""",
    },
    
    23: {  # American Dream - needs common_expectation
        "common_expectation": """<p>The American Dream for Indian engineers: H1B, high salary, eventual Green Card, and US citizenship. Your seniors did it. Your cousins are there. The path seems established: get into a US company, get sponsored, wait a few years, done.</p>

<p>The expectation: Multiply your salary 5x, build wealth in dollars, enjoy better quality of life. The US is where tech careers are made. India is for training; US is for earning.</p>

<p>The math seems obvious. But is it?</p>""",
    },
    
    24: {  # MBA - needs common_expectation
        "common_expectation": """<p>The MBA is India's golden ticket. IIM = success. "MBA se sab milega" (you'll get everything with an MBA). Parents push for it. Students prepare for CAT for years. The top B-school brand opens doors forever.</p>

<p>The expectation: Two years of study, then Rs 25-50 LPA jobs, fast-track to leadership, network for life. MBA transforms careers—from technical to management, from ordinary to elite.</p>

<p>The CAT score defines destinies. Or does it?</p>""",
    },
    
    25: {  # Remote Work - needs common_expectation
        "common_expectation": """<p>Remote work for US companies from India seems like the perfect arbitrage: US salaries, Indian costs. Rs 80 LPA to Rs 1.5 Cr while living in your hometown. Work in your pajamas. Attend meetings from your bedroom. Save 80% of your income.</p>

<p>The expectation: All the financial benefits of US employment without visa hassles, relocations, or lifestyle compromises. The best of both worlds, enabled by time zones and internet.</p>

<p>The numbers look too good to be true. Are they?</p>""",
    },
    
    26: {  # Side Hustles - needs common_expectation  
        "common_expectation": """<p>"Don't put all your eggs in one basket." "Build multiple income streams." "Your side hustle could become your main hustle." The side hustle gospel is preached everywhere. Financial independence requires diversification, and diversification requires side hustles.</p>

<p>The expectation: Work your day job, build something on the side, eventually have passive income or a business that replaces your salary. This is how modern wealth is built.</p>

<p>The success stories are endless. The failures are invisible.</p>""",
    },
    
    27: {  # Equity - needs common_expectation
        "common_expectation": """<p>Startup equity is the lottery ticket to early retirement. "Join early, get rich when we IPO." Stories of early Flipkart employees, Swiggy team members, and Zomato engineers making crores fuel the dream. Equity is how engineers become millionaires.</p>

<p>The expectation: Take a lower salary for equity, wait 4-5 years, cash out for life-changing money. It's the startup bargain—trade present salary for future wealth.</p>

<p>The stories make it sound like a reasonable bet. Is it?</p>""",
    },
    
    28: {  # Manager vs IC - needs common_expectation
        "common_expectation": """<p>The great career fork: management or individual contributor (IC). Managers lead people, ICs go deep technically. Both are valid paths. Companies say they value IC tracks as much as management. Staff Engineer = Engineering Manager in influence and pay.</p>

<p>The expectation: Choose the path that fits your personality. Love people? Go management. Love technology? Stay IC. Both lead to senior roles, good compensation, and fulfilling work.</p>

<p>The choice feels like a preference decision, not a trade-off. But is it?</p>""",
    }
}

print("Adding missing sections to THIN articles...")
for article_id, updates in expansions.items():
    try:
        article = Article.objects.get(id=article_id)
        for field, content in updates.items():
            setattr(article, field, content)
        article.save()
        print(f"  Updated ID {article_id}: {article.title[:40]}...")
    except Article.DoesNotExist:
        print(f"  Article ID {article_id} not found")
    except Exception as e:
        print(f"  Error with ID {article_id}: {e}")

print("\nRunning verification...")
