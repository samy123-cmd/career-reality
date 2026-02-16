from django.core.management.base import BaseCommand

from content.models import Article


class Command(BaseCommand):
    help = "Hardens published article content quality (internal links + meta descriptions)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Persist changes. Without this flag, runs in dry mode.",
        )

    def handle(self, *args, **options):
        apply_changes = options["apply"]
        updated_count = 0

        for article in Article.objects.filter(status="published").select_related("category"):
            changed = False

            contextual_links = (
                '<p>Related reads: '
                '<a href="/salary-reality/">Salary Reality</a>, '
                '<a href="/salary-calculator/">CTC Decoder</a>, '
                '<a href="/category/{slug}/">{name} careers</a>.'
                "</p>"
            ).format(slug=article.category.slug, name=article.category.name)

            if "/salary-reality/" not in (article.actual_reality or ""):
                article.actual_reality = (article.actual_reality or "") + contextual_links
                changed = True

            if "/salary-calculator/" not in (article.salary_reality or ""):
                article.salary_reality = (
                    (article.salary_reality or "")
                    + '<p>Estimate your real monthly take-home with the <a href="/salary-calculator/">CTC Decoder</a>.</p>'
                )
                changed = True

            if "/resignation-risk/" not in (article.stuck_point or ""):
                article.stuck_point = (
                    (article.stuck_point or "")
                    + '<p>If you are in this situation, use the <a href="/resignation-risk/">Resignation Risk Analyzer</a> before switching.</p>'
                )
                changed = True

            if len((article.meta_description or "").strip()) < 120:
                article.meta_description = (
                    f"{article.title} in India: salary reality, career trade-offs, and decision risks. "
                    "Data-backed analysis with practical next steps."
                )[:160]
                changed = True

            if changed:
                updated_count += 1
                self.stdout.write(f"- {article.slug}")
                if apply_changes:
                    article.save(update_fields=["actual_reality", "salary_reality", "stuck_point", "meta_description", "updated_at"])

        mode = "APPLY" if apply_changes else "DRY RUN"
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"{mode}: {updated_count} article(s) require updates."))
