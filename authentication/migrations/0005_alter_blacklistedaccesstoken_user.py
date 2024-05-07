# Generated by Django 5.0.4 on 2024-05-06 12:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_blacklistedaccesstoken_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blacklistedaccesstoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]