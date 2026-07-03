# Generated manually for data flywheel features

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("analyzer", "0006_phase1_data_foundation"),
    ]

    operations = [
        migrations.AddField(
            model_name="salarysubmission",
            name="source",
            field=models.CharField(
                blank=True,
                help_text="Attribution source (tool exit CTA)",
                max_length=40,
            ),
        ),
        migrations.AddField(
            model_name="salarysubmission",
            name="verification_status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("verified", "Verified"),
                    ("flagged", "Flagged"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
    ]
