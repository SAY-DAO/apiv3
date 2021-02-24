# Generated by Django 3.1.7 on 2021-02-24 17:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='normalized_email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.', regex='^\\+\\d{9,15}$')]),
        ),
    ]
