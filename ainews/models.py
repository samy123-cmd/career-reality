from django.db import models
from django.utils import timezone
from django.utils.text import slugify

import bleach

ALLOWED_SUMMARY_TAGS = [
    'p', 'h2', 'h3', 'ul', 'ol', 'li', 'strong', 'em', 'code', 'blockquote', 'a'
]
ALLOWED_SUMMARY_ATTRS = {
    'a': ['href', 'rel', 'target'],
}
ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']


class AITag(models.Model):
    """Categorizes AI news items (e.g., Model Release, Benchmark, Career Impact)."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, max_length=60)

    class Meta:
        verbose_name = "AI Tag"
        verbose_name_plural = "AI Tags"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('ai_news_by_tag', kwargs={'slug': self.slug})


class AINewsItem(models.Model):
    """An AI news item aggregated from RSS feeds or entered manually."""

    SIGNIFICANCE_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    FACT_CHECK_CHOICES = [
        ('pending', 'Pending'),
        ('in_review', 'In Review'),
        ('verified', 'Verified'),
    ]

    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, max_length=300)
    summary = models.TextField(help_text="2-3 sentence editorial summary of the development.")
    career_angle = models.TextField(
        blank=True,
        help_text="What this means for your career. The Career Reality editorial overlay."
    )
    source_name = models.CharField(max_length=100, help_text="e.g., OpenAI, VentureBeat, DeepMind")
    source_url = models.URLField(max_length=500, help_text="Link to the original article/announcement.")
    tags = models.ManyToManyField(AITag, blank=True, related_name='news_items')
    significance = models.CharField(
        max_length=10, choices=SIGNIFICANCE_CHOICES, default='medium',
        help_text="Editorial importance rating."
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    fact_check_status = models.CharField(max_length=20, choices=FACT_CHECK_CHOICES, default='pending')
    reviewed_by = models.CharField(max_length=120, blank=True)
    review_notes = models.TextField(blank=True)
    last_verified_at = models.DateTimeField(blank=True, null=True)
    event_date = models.DateTimeField(
        blank=True, null=True,
        help_text="Date when the external event/release happened."
    )
    reviewed_at = models.DateTimeField(
        blank=True, null=True,
        help_text="Latest editorial review/update timestamp."
    )
    published_at = models.DateTimeField(blank=True, null=True)
    fetched_at = models.DateTimeField(auto_now_add=True)
    external_id = models.CharField(
        max_length=500, unique=True, blank=True, null=True,
        help_text="RSS entry guid or API id for deduplication."
    )

    class Meta:
        verbose_name = "AI News Item"
        verbose_name_plural = "AI News Items"
        ordering = ['-published_at']
        indexes = [
            # Covers filter(status='published').order_by('-published_at') — hub, detail related
            models.Index(fields=['status', '-published_at'], name='ainews_status_pubdate_idx'),
            # Covers filter(status='published').order_by('-event_date', '-published_at') — hub, tag pages
            models.Index(fields=['status', '-event_date', '-published_at'], name='ainews_status_event_pub_idx'),
            # Covers sitemap query order_by('-reviewed_at', '-published_at')
            models.Index(fields=['status', '-reviewed_at'], name='ainews_status_reviewed_idx'),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:300]

        if self.summary:
            self.summary = bleach.clean(
                self.summary,
                tags=ALLOWED_SUMMARY_TAGS,
                attributes=ALLOWED_SUMMARY_ATTRS,
                protocols=ALLOWED_PROTOCOLS,
                strip=True,
            )
        if self.career_angle:
            self.career_angle = bleach.clean(
                self.career_angle,
                tags=['p', 'br', 'ul', 'ol', 'li', 'strong', 'em', 'code'],
                attributes={},
                protocols=ALLOWED_PROTOCOLS,
                strip=True,
            )

        if self.status == 'published':
            if not self.reviewed_at:
                self.reviewed_at = timezone.now()
            if not self.event_date:
                self.event_date = self.published_at or self.reviewed_at

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('ai_news_detail', kwargs={'slug': self.slug})


class AINewsFetchRun(models.Model):
    """Metrics and health status for one fetch_ai_news execution."""

    STATUS_CHOICES = [
        ('success', 'Success'),
        ('partial', 'Partial'),
        ('failed', 'Failed'),
    ]

    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='success')
    total_created = models.PositiveIntegerField(default=0)
    total_skipped = models.PositiveIntegerField(default=0)
    total_warnings = models.PositiveIntegerField(default=0)
    total_errors = models.PositiveIntegerField(default=0)
    source_count = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "AI News Fetch Run"
        verbose_name_plural = "AI News Fetch Runs"
        ordering = ['-started_at']

    def __str__(self):
        return f"Fetch run {self.started_at:%Y-%m-%d %H:%M:%S} ({self.status})"
