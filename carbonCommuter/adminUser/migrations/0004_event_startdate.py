# Generated by Django 5.0.2 on 2024-03-19 15:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminUser', '0003_event_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='startDate',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
