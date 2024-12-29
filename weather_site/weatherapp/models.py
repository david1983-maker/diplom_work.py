from django.db import models

# Create your models here.
class City(models.Model):

    name = models.CharField(max_length=40)

    # is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name