# Generated by Django 3.0.7 on 2020-10-23 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sbadmin', '0007_entry_log'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry_log',
            old_name='hour',
            new_name='day',
        ),
    ]
