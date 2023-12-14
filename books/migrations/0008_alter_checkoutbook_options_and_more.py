# Generated by Django 5.0 on 2023-12-12 11:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_alter_checkoutbook_due_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='checkoutbook',
            options={'ordering': ('-borrow_date',)},
        ),
        migrations.AlterField(
            model_name='checkoutbook',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2024, 1, 2, 11, 32, 28, 748643, tzinfo=datetime.timezone.utc)),
        ),
    ]