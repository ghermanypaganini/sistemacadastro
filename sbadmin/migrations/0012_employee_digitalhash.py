# Generated by Django 3.0.7 on 2020-10-29 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sbadmin', '0011_employee_digital'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='digitalHash',
            field=models.BinaryField(null=True),
        ),
    ]
