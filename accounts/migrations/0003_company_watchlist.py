# Generated manually for data flywheel features

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_phase1_data_foundation"),
        ("companies", "0002_phase1_data_foundation"),
        ("analyzer", "0006_phase1_data_foundation"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="salary_previews_month",
            field=models.CharField(blank=True, default="", max_length=7),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="salary_previews_used",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name="CompanyWatchlist",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "company",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="companies.company"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="company_watchlist",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "unique_together": {("user", "company")},
            },
        ),
        migrations.CreateModel(
            name="LayoffAlertLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sent_at", models.DateTimeField(auto_now_add=True)),
                (
                    "layoff_report",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="analyzer.layoffreport"),
                ),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "unique_together": {("user", "layoff_report")},
            },
        ),
    ]
