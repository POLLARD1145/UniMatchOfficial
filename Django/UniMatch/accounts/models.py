# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user model
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    grade_twelve_points = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username

# Model for hobbies
class Hobby(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Model for interests
class Interest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Model for education, including secondary and tertiary education
class Education(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100, blank=True, null=True)  # Degree field for tertiary education
    field = models.CharField(max_length=100, blank=True, null=True)   # Field of study for tertiary education
    institution = models.CharField(max_length=150)                    # School or institution name
    year = models.IntegerField()                                      # Year of graduation or completion
    grade_twelve_points = models.IntegerField(blank=True, null=True)  # Grade 12 points for secondary education

    def __str__(self):
        if self.degree:
            return f"{self.degree} in {self.field} from {self.institution} ({self.year})"
        return f"Secondary School: {self.institution} - Grade 12 Points: {self.grade_twelve_points} ({self.year})"
