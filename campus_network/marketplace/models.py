from django.db import models
from django.contrib.auth.models import User
from pgvector.django import VectorField

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.CharField(max_length=100)
    bio = models.TextField(help_text="Tell us about yourself and what you're looking for.")

    #The ai field
    embedding = VectorField(dimensions=1536, null= True, blank=True)

    def __str__(self):
        return f"{self.user.first_name}'s profile"
    

class Opportunity(models.Model):
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    location = models.CharField(max_length=200, help_text="e.g., Red Hook, Kingston, On-Campus")
    description = models.TextField()
    is_paid = models.BooleanField(default=False)

    #The ai field
    embedding = VectorField(dimensions=1536, null=True, blank=True)

    def __str__(self):
        return f'{self.title} at {self.orginization}'
    

class Event(models.Model):
    title = models.CharField(max_length=200)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=150)
    description = models.TextField()  

    #The Ai field
    embedding = VectorField(dimensions=1536, null = True, blank = True)

    def __str__(self):
        return f"{self.title} at {self.location}"

