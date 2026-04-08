# Generated migration to add patient_name field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0009_fix_appointment_patient_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='patient_name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
