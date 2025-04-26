from django.db import models

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to="images/")

class DImage(models.Model):
    oimg = models.ForeignKey(Image,on_delete=models.CASCADE,null=True)
    dimg = models.ImageField(upload_to="dimages/")