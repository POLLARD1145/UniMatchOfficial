from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    grade_twelve_points = models.IntegerField(max_length=2,blank=True,null=True)

    def __str__(self):
        return self.username

#models for other user details
class Hobby(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)

    #define the to string to return the name when the model is called
    def __str__(self):
        return self.name
class Interest(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(CustomUser,on_delete = models.CASCADE)

    #define the to string to return the name when the model is called
    def __str__(self):
        return self.name