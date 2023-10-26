from django.contrib.auth.models import User
from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.CharField(max_length=1000)
    time = models.IntegerField()
    process = models.CharField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name




