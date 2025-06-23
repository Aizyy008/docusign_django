from django.db import models
from django.contrib.auth.models import User

class EnvelopeStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    envelope_id = models.CharField(max_length=100)
    signed = models.BooleanField(default=False)
