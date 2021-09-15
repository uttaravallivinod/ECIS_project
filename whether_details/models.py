from django.contrib.gis.db import models

# Create your models here.
class Whether(models.Model):
    location=models.PointField()
    date=models.DateTimeField(auto_now_add=True)
    city=models.CharField(max_length=100,default="Not Updated")

