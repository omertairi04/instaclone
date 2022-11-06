from django.db import models
import uuid

from users.models import Profile

class Posts(models.Model):
    owner = models.ForeignKey(Profile , on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    caption = models.TextField(blank=True , null=True)
    location = models.ForeignKey('Location' , on_delete=models.CASCADE,blank=True , null=True)
    post_image = models.ImageField(default='')
    # likes
    # comments
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , 
                        primary_key=True , editable=False)

    def __str__(self):
        return self.title

class Location(models.Model):
    city = models.CharField(max_length=255,blank=True , null=True)
    country = models.CharField(max_length=255,blank=True , null=True)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , 
                        primary_key=True , editable=False)
    def __str__(self):
        return f'{self.city} - {self.country}'