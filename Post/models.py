from datetime import datetime
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.

class Posting(models.Model):
    post_idx =  models.AutoField(primary_key=True)
    id = models.ForeignKey('User.User', on_delete = models.CASCADE, db_column="id")
    title = models.CharField(max_length=255,null=True)
    body = models.TextField(null=True)
    pic	= models.ImageField()
    date = models.DateTimeField(default = datetime.now)
    visualhearing = models.IntegerField() 
    class Meta:
        db_table = 'Posting'
        app_label = 'Post'
        managed = False



class Chatting(models.Model):
    chatting_index = models.AutoField(primary_key=True)
    post_idx = models.ForeignKey('Posting', on_delete = models.CASCADE, db_column="post_idx")
    username = models.CharField(max_length=150, blank=True)
    date = models.DateTimeField(default = datetime.now)
    chatting =  models.TextField(null=True)
    class Meta:
        db_table = 'Chatting'
        app_label ='Post'
        managed = False