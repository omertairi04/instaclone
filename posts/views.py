from django.shortcuts import render

from .models import Posts

def index(request):
    posts = Posts.objects.all()
    context = {
        'posts':posts
    }
    return render(request , 'index.html',context)

def singlePost(request , pk):
    post = Posts.objects.get(id=pk)
    context = {
        'post':post
    }
    return render(request,'posts/singePost.html',context)
