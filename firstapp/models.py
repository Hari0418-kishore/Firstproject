from django.db import models

# Create your models here.
class movies(models.Model):
    img : models.ImageField( upload_to = 'pics')
    title = models.CharField(max_length=100)
class slides:
    img : str
