# Generated by Django 4.2 on 2023-04-18 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jims_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddInmate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=80)),
                ('middle_initial', models.CharField(blank=True, max_length=1, null=True)),
                ('last_name', models.CharField(max_length=80)),
                ('date_of_birth', models.CharField(max_length=10)),
                ('place_of_birth', models.CharField(max_length=25)),
                ('country', models.CharField(max_length=80)),
                ('nationality', models.CharField(max_length=80)),
                ('sex', models.CharField(max_length=10)),
                ('hair_color', models.CharField(max_length=20)),
                ('eye_color', models.CharField(max_length=20)),
                ('height_feet', models.PositiveIntegerField()),
                ('height_inches', models.PositiveIntegerField()),
                ('weight', models.CharField(max_length=10)),
                ('alias', models.CharField(blank=True, max_length=80, null=True)),
                ('blemishes', models.CharField(blank=True, max_length=200, null=True)),
                ('primary_add', models.CharField(max_length=200)),
                ('temp_add', models.CharField(blank=True, max_length=200, null=True)),
                ('drivers_license_num', models.CharField(max_length=80)),
                ('drivers_license_state', models.CharField(max_length=2)),
            ],
        ),
    ]
