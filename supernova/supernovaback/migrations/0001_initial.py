# Generated by Django 4.2.7 on 2024-07-21 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('year', models.IntegerField(primary_key=True, serialize=False)),
                ('semester', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(blank=True, max_length=100, null=True)),
                ('time_table', models.JSONField()),
                ('empty_time', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('pet_code', models.IntegerField(default=0)),
                ('pet_xp', models.IntegerField(default=0)),
            ],
        ),
    ]
