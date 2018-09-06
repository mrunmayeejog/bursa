from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Entry(models.Model):
    """
    Entry model definition
    """
    Entry_TYPE = (
        ('D', 'Debit'),
        ('C', 'Credit')
    )

    id = models.CharField(max_length=60, primary_key=True)
    amount = models.FloatField()
    type = models.CharField(max_length=1, choices=Entry_TYPE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    category = models.CharField(max_length=60, blank=False, unique=False)
    place = models.CharField(max_length=60, blank=False, unique=False)

    def __str__(self):
        return self.id