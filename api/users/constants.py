from django.db import models





class Gender(models.TextChoices):
    FEMALE = 'female'
    MALE = 'male'
    OTHER = 'other'
