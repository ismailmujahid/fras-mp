from django.db import models
# Create your models here.


class admin_details(models.Model):
    aname  = models.CharField(max_length=30)
    apass  = models.CharField(max_length=30)
    class Meta:
        db_table = 'admin_details'

class userDetails(models.Model):
    F_name = models.CharField(max_length=100)
    age  = models.CharField(max_length=30)
    phone= models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=100,default=None)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    Class = models.CharField(max_length=100)
    images = models.ImageField(default=None,max_length=200)
    class Meta:
        db_table = 'userDetails'

class attendance(models.Model):
    name = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    class Meta:
        db_table = 'attendance'



