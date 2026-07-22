import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        # --- Timestamps (nullable so existing rows don't need a backfill default) ---
        migrations.AddField(
            model_name='company',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='placement',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='placement',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='internship',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='internship',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),

        # --- CTC validation ---
        migrations.AlterField(
            model_name='placement',
            name='ctc_lpa',
            field=models.FloatField(
                help_text='CTC in Lakhs Per Annum',
                validators=[django.core.validators.MinValueValidator(0.0)],
            ),
        ),

        # --- Stipend split: stipend_monthly (string) -> is_paid (bool) + stipend_amount (int) ---
        migrations.AddField(
            model_name='internship',
            name='is_paid',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='internship',
            name='stipend_amount',
            field=models.PositiveIntegerField(
                blank=True, null=True,
                help_text='Monthly stipend in INR. Leave blank if unpaid.',
            ),
        ),
        # Data migration: parse the old stipend_monthly string into the two new fields
        # before the column is dropped, so no existing data is lost.
        migrations.RunPython(
            code=lambda apps, schema_editor: _migrate_stipend_data(apps, schema_editor),
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name='internship',
            name='stipend_monthly',
        ),

        # --- Uniqueness constraints (one placement / internship record per student+company) ---
        migrations.AddConstraint(
            model_name='placement',
            constraint=models.UniqueConstraint(
                fields=('student', 'company'), name='unique_placement_per_student_company'
            ),
        ),
        migrations.AddConstraint(
            model_name='internship',
            constraint=models.UniqueConstraint(
                fields=('student', 'company'), name='unique_internship_per_student_company'
            ),
        ),
    ]


def _migrate_stipend_data(apps, schema_editor):
    Internship = apps.get_model('tracker', 'Internship')
    for internship in Internship.objects.all():
        raw = (internship.stipend_monthly or '').strip()
        if raw.lower() == 'unpaid':
            internship.is_paid = False
            internship.stipend_amount = None
        else:
            try:
                internship.is_paid = True
                internship.stipend_amount = int(float(raw))
            except (ValueError, TypeError):
                internship.is_paid = True
                internship.stipend_amount = None
        internship.save(update_fields=['is_paid', 'stipend_amount'])