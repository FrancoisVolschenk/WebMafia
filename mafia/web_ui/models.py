from email.policy import default
from django.db import models

class Game(models.Model):
    code = models.CharField(max_length=10, unique=True)
    started = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)

    def __str__(self) -> str:
        return ("{}: Started({}), Ended({})".format(self.code, self.started, self.ended))

class Role(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    playable = models.BooleanField(default=True)
    optional = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class Player(models.Model):
    class Meta:
        unique_together = (('name', 'game'))
    name = models.CharField(max_length=25, unique=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_host = models.BooleanField(default=False)

    def __str__(self) -> str:
        return (self.name)