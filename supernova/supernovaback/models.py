from django.db import models
import json


class User(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    pet_code = models.IntegerField(default=0)
    pet_xp = models.IntegerField(default=0)
    pet_ptg = models.FloatField(default=0)
    timer_recent = models.IntegerField(null=True)
    timer_on = models.BooleanField(default=False)
    timer_sum = models.IntegerField(default=0)
    

    def __str__(self):
        return self.id


class Semester(models.Model):
    year = models.IntegerField(primary_key=True)
    semester = models.IntegerField()
    password = models.CharField(max_length=255)


class TimeSlot(models.Model):
    userid = models.CharField(max_length=255, primary_key=True)
    time_table = models.JSONField()
    empty_time = models.IntegerField()  # 0 to 287 (representing 5-minute intervals from 00:00 to 23:55)

    def save(self, *args, **kwargs):
        self.time_table = json.dumps(self.time_table)
        super().save(*args, **kwargs)


class Quiz(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)


class Answer(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.CharField(max_length=255)
    quiz_id = models.IntegerField()

class Category(models.Model):
    read = models.IntegerField(default=0)
    walk = models.IntegerField(default=0)
    movie = models.IntegerField(default=0)
    workout = models.IntegerField(default=0)
    study = models.IntegerField(default=0)
    sleep = models.IntegerField(default=0)