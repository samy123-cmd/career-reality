from django.db import models
from django.utils.text import slugify

class Author(models.Model):
    name = models.CharField(max_length=100, help_text="Real human name (Proof of life)")
    display_name = models.CharField(max_length=100, help_text="Public brand-safe name")
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='authors/', blank=True, null=True)
    linkedin_url = models.URLField(help_text="Critical Trust Signal")
    experience_summary = models.CharField(max_length=255, blank=True, help_text="e.g. '10+ years in Fintech Product Management'")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.display_name

class Category(models.Model):
    name = models.CharField(max_length=100)
    name_hi = models.CharField(max_length=100, blank=True, null=True, help_text="Hindi Translation")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    description_hi = models.TextField(blank=True, null=True, help_text="Hindi Translation")
    order = models.PositiveIntegerField(default=0, help_text="Display order (0 = first)")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('category_detail', kwargs={'slug': self.slug})

class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    title_hi = models.CharField(max_length=200, blank=True, null=True, help_text="Hindi Translation")
    slug = models.SlugField(unique=True, max_length=200)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Strict Content Structure
    target_persona = models.TextField(help_text="Who is this specific article for?")
    target_persona_hi = models.TextField(blank=True, null=True, help_text="Hindi Translation")
    who_should_avoid = models.TextField(help_text="Trust Signal: Who should NOT pursue this?")
    who_should_avoid_hi = models.TextField(blank=True, null=True, help_text="Hindi Translation")
    common_expectation = models.TextField(help_text="The Myth / What people think")
    common_expectation_hi = models.TextField(blank=True, null=True, help_text="Hindi Translation")
    actual_reality = models.TextField(help_text="The Truth / What it's actually like")
    actual_reality_hi = models.TextField(blank=True, null=True, help_text="Hindi Translation")
    salary_reality = models.TextField(help_text="Real data tables/ranges. No hype.")
    salary_reality_hi = models.TextField(blank=True, null=True, help_text="Hindi Translation")
    stuck_point = models.TextField(help_text="Where most people fail or plateau")
    stuck_point_hi = models.TextField(blank=True, null=True, help_text="Hindi Translation")
    verdict = models.TextField(help_text="Final honest conclusion")
    verdict_hi = models.TextField(blank=True, null=True, help_text="Hindi Translation")
    
    # SEO & Metadata
    meta_title = models.CharField(max_length=60, help_text="SEO Title (max 60 chars)")
    meta_title_hi = models.CharField(max_length=60, blank=True, null=True, help_text="Hindi Translation")
    meta_description = models.CharField(max_length=160, help_text="SEO Description (max 160 chars)")
    meta_description_hi = models.CharField(max_length=160, blank=True, null=True, help_text="Hindi Translation")
    published_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_reality_check = models.DateField(blank=True, null=True, help_text="Date of last factual review")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('article_detail', kwargs={'slug': self.slug})

    class Meta:
        indexes = [
            # Covers filter(status='published').order_by('-published_at')
            models.Index(fields=['status', '-published_at'], name='article_status_pubdate_idx'),
            # Covers filter(category=..., status='published').order_by('-published_at')
            models.Index(fields=['status', 'category', '-published_at'], name='article_status_cat_idx'),
            # Covers filter(status='published').order_by('-updated_at') (sitemap, home recent_updates)
            models.Index(fields=['status', '-updated_at'], name='article_status_updated_idx'),
        ]
