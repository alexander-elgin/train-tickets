from django.db import models


class Train(models.Model):
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.id
