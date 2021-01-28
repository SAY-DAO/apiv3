from django.db import models


EMAIL = 'E'
MOBILE = 'M'
DESTINATION_CHOICES = [(EMAIL, 'EMail Address'), (MOBILE, 'Mobile Number')]


class Gender(models.TextChoices):
    FEMALE = 'female'
    MALE = 'male'
    OTHER = 'other'
