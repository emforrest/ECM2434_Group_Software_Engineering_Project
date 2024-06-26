# Generated by Django 5.0.2 on 2024-02-27 22:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Journey',
            fields=[
                ('time_logged', models.DateTimeField(auto_created=True)),
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, unique=True)),
                ('distance', models.FloatField()),
                ('destination', models.CharField(max_length=128)),
                ('transport', models.CharField(max_length=16)),
                ('origin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_saving', models.FloatField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
