from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    # add additional fields here
    post = models.ForeignKey('builder.Post', null=True, default=None, on_delete=models.SET_DEFAULT)
    science_degree  = models.ForeignKey('builder.ScienceDegree', null=True, default=None, on_delete=models.SET_NULL)
    science_title = models.ForeignKey('builder.ScienceTitle', null=True, default=None, on_delete=models.SET_NULL)
    salary = models.FloatField(null=True, default=1)
    adopted_fields = models.ForeignKey('builder_auth.CustomUser', null=True, default=None, on_delete=models.SET_NULL)

    def __str__(self):
        return self.email