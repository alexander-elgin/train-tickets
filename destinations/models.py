from django.db import models


class Destination(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
