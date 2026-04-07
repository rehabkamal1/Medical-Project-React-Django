# Generated manually to fix missing patient_id column

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0008_merge_20250614_1911'),
        ('patients', '0003_merge_20250614_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='patients.patient'),
            preserve_default=False,
        ),
    ]
