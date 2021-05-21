#!/usr/bin/env python3
 
from fakedjango import models

class Ox(models.Model):
    horn_length = models.IntegerField()

    class Meta:
        ordering = ['horn_length']
        verbose_name_plural = 'oxen'

print(Ox.Meta.__name__)
print(Ox.Meta.__qualname__)
