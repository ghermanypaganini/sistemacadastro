# Generated by Django 3.0.7 on 2020-06-11 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sbadmin', '0003_auto_20200611_0129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='registration_code',
            field=models.IntegerField(error_messages={'unique': 'This email has already been registered.'}, unique=True, verbose_name='Matrícula'),
        ),
    ]
