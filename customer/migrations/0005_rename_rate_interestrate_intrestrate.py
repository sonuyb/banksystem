# Generated by Django 5.0.4 on 2024-05-06 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_recurringdepositaccount_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interestrate',
            old_name='rate',
            new_name='intrestrate',
        ),
    ]
