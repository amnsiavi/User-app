from django.db import models
from datetime import datetime

# Create your models here.
class UserAppModel(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.JSONField(default=dict(street='',suite='',city='',zip_code='',geo_location=dict(lat=0.0,lng=0.0)))
    phone = models.CharField(max_length=20)
    website = models.URLField()
    company = models.JSONField(default=dict(name='',catchPhrase='',BS=''))
    created = models.DateTimeField(default=datetime.now())
    updated = models.DateTimeField(default=datetime.now())
    


    def __str__(self):
        return self.username

