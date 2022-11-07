from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required

from .models import Posts
from .forms import PostForm

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

@login_required(login_url='login')
def createPost(request):
    profile = request.user.profile
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST , request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.owner = profile
            user.save()

            return redirect('index')
    
    context = {
        'form':form
    }
    return render(request,'posts/createPost.html',context)

@login_required(login_url='login')
def editPost(request , pk):
    post = Posts.objects.get(id=pk)
    form = PostForm(instance=post)
    if request.method=='POST':
        form = PostForm(request.POST , request.FILES , instance=post)
        if form.is_valid():
            form.save()
            return redirect('index')
    
    context = {
        'form':form
    }
    return render(request , 'posts/editPost.html',context)

@login_required(login_url='login')
def deletePost(request , pk):
    post = Posts.objects.get(id=pk)
    post.delete()
    return redirect('index')
    return render(request , 'posts/delete.html')

