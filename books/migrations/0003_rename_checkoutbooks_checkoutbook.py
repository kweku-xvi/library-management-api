# Generated by Django 5.0 on 2023-12-11 12:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_checkoutbooks'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CheckoutBooks',
            new_name='CheckoutBook',
        ),
    ]
