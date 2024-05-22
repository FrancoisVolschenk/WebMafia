from email.policy import default
from django.db import models

class Game(models.Model):
    code = models.CharField(max_length=10, unique=True)
    started = models.BooleanField(default=False)

class Role(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    playable = models.BooleanField(default=True)


class Player(models.Model):
    name = models.CharField(max_length=25, unique=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_host = models.BooleanField(default=False)