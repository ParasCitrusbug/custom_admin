# Generated by Django 4.1.7 on 2023-03-02 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeedata',
            name='phone_number',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]
