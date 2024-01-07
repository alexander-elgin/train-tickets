from django.db import models

from trains.models import Train


class Carriage(models.Model):
    id = models.AutoField(primary_key=True)
    train = models.ForeignKey(Train, on_delete=models.CASCADE, default=None)
    sleeping = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.id
