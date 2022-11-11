from django.db import models
import uuid
from django.contrib.auth.models import User

from users.models import Profile

class Posts(models.Model):
    owner = models.ForeignKey(Profile , on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    caption = models.TextField(blank=True , null=True)
    location = models.ForeignKey('Location' , on_delete=models.CASCADE,blank=True , null=True)
    post_image = models.ImageField(default='')
    likes = models.IntegerField(default=0)
    comments = models.ForeignKey('Comment',on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , 
                        primary_key=True , editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

class Comment(models.Model):
    user = models.ForeignKey(User , null=True,blank=True , on_delete=models.CASCADE)
    post = models.ForeignKey(Posts ,null=True,blank=True , on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , 
                        primary_key=True , editable=False)

    def __str__(self):
        return self.body

class Location(models.Model):
    city = models.CharField(max_length=255,blank=True , null=True)
    country = models.CharField(max_length=255,blank=True , null=True)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , 
                        primary_key=True , editable=False)
    def __str__(self):
        return f'{self.city} - {self.country}'

class Likes(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='user_likes')
    post = models.ForeignKey(Posts , on_delete=models.CASCADE , related_name='post_likes')


