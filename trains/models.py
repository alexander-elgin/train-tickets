from django.db import models


class Train(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return str(self.id)
