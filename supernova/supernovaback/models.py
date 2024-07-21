from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255,null=True)
    id = models.IntegerField(primary_key=True)
    pet = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name
