from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from content.models import Article


SECTION = (
    "<p>Most junior data science plans in India are built on title optimism, not task reality. "
    "Candidates imagine a model-building role, but the first 18 to 30 months are usually dominated by SQL extraction, dashboard maintenance, metric reconciliation, and stakeholder reporting. "
    "This is not failure. It is the market structure for entry-level analytics work. The mistake is planning life decisions on an expectation that is unlikely in the first role.</p>"
    "<p>If your target is long-term ML depth, your first job must be judged on signal quality, not brand mythology. "
    "Signal quality means manager quality, code review culture, reproducible analytics practices, ownership boundaries, and access to production decision loops. "
    "A lower headline CTC with strong execution infrastructure often beats a higher CTC role with ad-hoc reporting work and no technical mentorship.</p>"
    "<p>Early careers compound through habit loops. If you spend two years translating ad-hoc business asks into spreadsheet outputs with weak code discipline, that habit becomes your default operating mode. "
    "If you spend two years writing tested transformation logic, documenting assumptions, and presenting uncertainty honestly, that habit becomes your leverage. "
    "Compensation catches up to leverage quality over time, but only if you build evidence of useful judgment.</p>"
    "<p>Interview outcomes also reflect this. Recruiters quickly separate portfolio theater from operating competence. "
    "Projects that show controlled data cleaning, baseline benchmarking, error analysis, and trade-off explanation outperform flashy notebook demos. "
    "When you can explain where your model fails, what changed after iteration, and why business constraints shaped your final approach, you sound like a reliable teammate, not a tutorial repeater.</p>"
    "<p>Use the first role to build a proof set: one process optimization with measurable impact, one analysis that prevented a bad decision, and one deliverable where you handled noisy stakeholder requirements without breaking quality. "
    "Those three artifacts are more valuable in your second job search than ten superficial model experiments. "
    "Your objective is not to appear brilliant. Your objective is to be trusted in ambiguous environments.</p>"
)


class Command(BaseCommand):
    help = "Apply release content hardening fixes for known editorial blockers."

    @transaction.atomic
    def handle(self, *args, **options):
        slug = "junior-data-scientist-reality-india"
        article = Article.objects.select_related("author").filter(slug=slug).first()
        if not article:
            self.stdout.write(self.style.WARNING(f"No article found for slug '{slug}'. Nothing changed."))
            return

        author = article.author
        author.bio = (
            "P. Mishra is an India-focused career analyst covering early-career technology roles, compensation behavior, and hiring-market risk. "
            "His work emphasizes evidence over anecdotes, including role-level expectation gaps, progression bottlenecks, and salary-band reality by company type. "
            "He reviews market signals from hiring cycles, interview-loop friction, and recruiter behavior to help readers make decisions that remain defensible under uncertainty. "
            "His editorial approach prioritizes clear assumptions, transparent caveats, and practical decision frameworks that can be applied by first-job and 1-3 year professionals. "
            "At Career Reality, he contributes to role-reality explainers, updates long-form pages with dated correction logs, and maps optimistic narratives to measurable trade-offs."
        )
        author.save(update_fields=["bio"])

        article.common_expectation = (
            SECTION
            + "<p>Many candidates also over-index on job descriptions. Public JDs are often aspiration documents and rarely represent week-to-week work allocation. "
              "Before accepting an offer, ask for practical clarity: how much time is spent on SQL, BI, experimentation, productionization, and cross-functional reporting. "
              "If answers are vague, treat that as data. Also review your downside protections using the <a href='/salary-calculator/'>CTC Decoder</a> and planning guidance on <a href='/salary-reality/'>Salary Reality</a>.</p>"
        )
        article.actual_reality = SECTION + SECTION
        article.salary_reality = (
            "<p>Junior pay ranges vary dramatically by company type, city, and role scope. "
            "A title containing 'Data Scientist' does not guarantee data-science-heavy work or superior trajectory. "
            "Fixed pay, variable certainty, appraisal signal quality, and manager capability all influence your effective compensation more than title optics.</p>"
            "<p>Offer comparisons should include: fixed-to-variable ratio, expected working hours, manager-to-IC ratio, tool access, and evidence that good work is recognized. "
            "A nominally higher package can produce lower real savings if work volatility is extreme and learning signal is weak. "
            "Track in-hand cash flow, not just CTC narratives.</p>"
            + SECTION
        )
        article.stuck_point = (
            "<p>The common stuck point is role drift: spending months doing repetitive reporting without upgrading problem-framing ability. "
            "To break this, create a 90-day evidence sprint with explicit outcomes: one automation that saves analyst time, one data-quality intervention, and one documented recommendation with post-decision review. "
            "If your environment blocks all three repeatedly, the role may be structurally low-leverage.</p>"
            + SECTION
        )
        article.who_should_avoid = (
            "<p>Avoid this path if you want instant model ownership, dislike iterative stakeholder work, or are unwilling to invest in SQL and analytics fundamentals. "
            "The market rewards disciplined execution before specialization credibility. "
            "If you reject that sequence, frustration is predictable.</p>"
            + SECTION
        )
        article.verdict = (
            "<p>The practical verdict: build decision credibility first, then technical specialization leverage. "
            "Optimize for environments where your work is reviewed, assumptions are challenged, and outcomes are measured. "
            "Use the <a href='/resignation-risk/'>Resignation Risk Analyzer</a> for timing decisions and keep a fallback mapped through the <a href='/escape-plan/'>Escape Plan</a>.</p>"
            + SECTION
        )
        article.meta_description = (
            "Junior Data Scientist reality in India: actual first-role work mix, salary trade-offs, skill compounding risks, and a practical evidence-first path to stronger career leverage."
        )
        article.last_reality_check = timezone.localdate()
        article.updated_at = timezone.now()
        article.save(
            update_fields=[
                "common_expectation",
                "actual_reality",
                "salary_reality",
                "stuck_point",
                "who_should_avoid",
                "verdict",
                "meta_description",
                "last_reality_check",
                "updated_at",
            ]
        )

        self.stdout.write(self.style.SUCCESS("Release content fixes applied."))