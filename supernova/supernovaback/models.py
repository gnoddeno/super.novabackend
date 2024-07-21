from django.db import models

class User(models.Model):
    id = models.CharField(max_length=255,primary_key=True)
    pet_code = models.IntegerField(default=0)
    pet_xp = models.IntegerField(default=0)

    def __str__(self):
        return self.id

class Semester(models.Model):
    year = models.IntegerField(primary_key=True)
    semester = models.IntegerField()