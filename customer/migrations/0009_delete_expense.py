# Generated by Django 5.0.4 on 2024-05-07 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_remove_budget_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Expense',
        ),
    ]
