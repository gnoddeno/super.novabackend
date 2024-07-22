# Generated by Django 4.2.7 on 2024-07-22 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=255)),
                ('quiz_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.IntegerField(default=0)),
                ('walk', models.IntegerField(default=0)),
                ('movie', models.IntegerField(default=0)),
                ('workout', models.IntegerField(default=0)),
                ('study', models.IntegerField(default=0)),
                ('sleep', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('content', models.CharField(max_length=255)),
                ('answer', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('year', models.IntegerField(primary_key=True, serialize=False)),
                ('semester', models.IntegerField()),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('userid', models.CharField(max_length=255, primary_key=True, serialize=False)),
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
                ('pet_ptg', models.FloatField(default=0)),
                ('timer_recent', models.IntegerField(null=True)),
                ('timer_on', models.BooleanField(default=False)),
                ('timer_sum', models.IntegerField(default=0)),
            ],
        ),
    ]