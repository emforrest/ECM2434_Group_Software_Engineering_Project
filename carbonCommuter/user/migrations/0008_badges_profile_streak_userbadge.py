# Generated by Django 5.0.2 on 2024-03-16 16:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0007_alter_follower_unique_together"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Badges",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        default=0,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(default="", max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name="profile",
            name="streak",
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name="UserBadge",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "badge",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="user.badges"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]