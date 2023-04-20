# Generated by Django 4.2 on 2023-04-20 02:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('position', models.CharField(choices=[('officer', 'officer'), ('booking_clerk', 'booking_clerk'), ('supervisor', 'supervisor'), ('release_clerk', 'release_clerk')], max_length=25)),
                ('user_status', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('account_number', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('inmate_id', models.CharField(max_length=200)),
                ('balance', models.FloatField()),
            ],
        ),
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
        migrations.CreateModel(
            name='BookingClerk',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('booking_clerk_id', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Officer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('officer_id', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ReleaseClerk',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('release_clerk_id', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('supervisor_id', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionDetails',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('transaction_type', models.CharField(max_length=2)),
                ('transaction_amount', models.FloatField()),
                ('transaction_date', models.DateTimeField()),
                ('account_number_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jims_app.accounts')),
            ],
        ),
    ]
