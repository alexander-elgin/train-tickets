from django.db import models


class Destination(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.name
