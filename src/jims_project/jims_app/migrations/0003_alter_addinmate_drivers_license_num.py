# Generated by Django 4.2 on 2023-04-20 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jims_app', '0002_addinmate_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addinmate',
            name='drivers_license_num',
            field=models.CharField(max_length=80, unique=True),
        ),
    ]