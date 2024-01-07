from django.db import models

from trains.models import Train


class Carriage(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    train = models.ForeignKey(Train, on_delete=models.CASCADE, default=None, db_index=True)
    sleeping = models.BooleanField(default=False, db_index=True)
    active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.id
