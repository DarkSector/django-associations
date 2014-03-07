from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Demo(models.Model):

    name = models.CharField(max_length=150, unique=True)
    pub_date = models.DateTimeField(auto_now=True)
    pub_author = models.ForeignKey(User)