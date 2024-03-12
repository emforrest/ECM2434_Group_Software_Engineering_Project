# Generated by Django 5.0.2 on 2024-03-12 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_journey_direction_remove_journey_off_campus_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='total_saving',
        ),
        migrations.AddField(
            model_name='journey',
            name='estimated_time',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
