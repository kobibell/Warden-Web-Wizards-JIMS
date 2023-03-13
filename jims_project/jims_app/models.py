from django.db import models

# Create your models here.
class login(models.Model):
    """
    Create a login model (database) with the user_name, password, and email as its feilds
    """
    user_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)