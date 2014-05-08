from django.db import models

# Create your models here.

class Writer(models.Model):
    class Meta:
        permissions = (
            ('can_write', 'Can write letters'),
        )
