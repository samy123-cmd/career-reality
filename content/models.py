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
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (0 = first)")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Strict Content Structure
    target_persona = models.TextField(help_text="Who is this specific article for?")
    who_should_avoid = models.TextField(help_text="Trust Signal: Who should NOT pursue this?")
    common_expectation = models.TextField(help_text="The Myth / What people think")
    actual_reality = models.TextField(help_text="The Truth / What it's actually like")
    salary_reality = models.TextField(help_text="Real data tables/ranges. No hype.")
    stuck_point = models.TextField(help_text="Where most people fail or plateau")
    verdict = models.TextField(help_text="Final honest conclusion")
    
    # SEO & Metadata
    meta_title = models.CharField(max_length=60, help_text="SEO Title (max 60 chars)")
    meta_description = models.CharField(max_length=160, help_text="SEO Description (max 160 chars)")
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
