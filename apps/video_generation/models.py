from django.db import models


class Character(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="characters/")
    voice = models.CharField(max_length=200)

    def __str__(self):
        return self.name
