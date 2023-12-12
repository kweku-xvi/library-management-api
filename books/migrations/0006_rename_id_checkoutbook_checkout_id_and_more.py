# Generated by Django 5.0 on 2023-12-12 11:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_checkoutbook_due_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkoutbook',
            old_name='id',
            new_name='checkout_id',
        ),
        migrations.AlterField(
            model_name='checkoutbook',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2024, 1, 2, 11, 15, 15, 70933, tzinfo=datetime.timezone.utc)),
        ),
    ]
