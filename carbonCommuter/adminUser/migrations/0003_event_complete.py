# Generated by Django 5.0.2 on 2024-03-19 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminUser', '0002_event_progress'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]