# Generated by Django 3.1.7 on 2021-03-23 09:46

from django.db import migrations
from django.db import models

import authentication.models
import common.mixins.timestamp


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('session', models.TextField(verbose_name='Session Passed')),
                ('token', models.TextField(verbose_name='JWT Token passed')),
            ],
            options={
                'verbose_name': 'Authentication Transaction',
                'verbose_name_plural': 'Authentication Transactions',
            },
            bases=(models.Model, common.mixins.timestamp.TimestampMixin),
        ),
        migrations.CreateModel(
            name='OTPValidation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('destination', models.CharField(max_length=254, unique=True, verbose_name='Destination Address (Mobile/EMail)')),
                ('destination_type', models.CharField(choices=[('email', 'EMail Address'), ('phone', 'Phone Number')], default='email', max_length=10, verbose_name='Destination Type')),
                ('is_verified', models.BooleanField(default=False, verbose_name='Is Verified')),
                ('secret', models.CharField(max_length=128, verbose_name='OTP Secret')),
                ('send_counter', models.IntegerField(default=0, verbose_name='OTP Sent Counter')),
                ('verify_date', models.DateTimeField(null=True, verbose_name='Date Verified')),
            ],
            options={
                'verbose_name': 'OTP Validation',
                'verbose_name_plural': 'OTP Validations',
            },
            bases=(models.Model, common.mixins.timestamp.TimestampMixin),
        ),
        migrations.CreateModel(
            name='ResetPassword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=10, unique=True)),
                ('destination', models.CharField(max_length=254, unique=True, verbose_name='Destination Address (Mobile/EMail)')),
                ('destination_type', models.CharField(choices=[('email', 'EMail Address'), ('phone', 'Phone Number')], default='email', max_length=10, verbose_name='Destination Type')),
                ('expired_at', models.DateTimeField(default=authentication.models.get_reset_password_expire_date)),
                ('is_used', models.BooleanField(default=False)),
            ],
            bases=(models.Model, common.mixins.timestamp.TimestampMixin),
        ),
    ]
