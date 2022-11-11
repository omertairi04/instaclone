from django.contrib import admin

from .models import Posts , Location , Comment

admin.site.register(Posts)
admin.site.register(Location)
admin.site.register(Comment)
