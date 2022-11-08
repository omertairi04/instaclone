from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Posts
from .forms import PostForm

def index(request):
    posts = Posts.objects.all()
    paginator = Paginator(posts , 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts':posts,
        'paginator':paginator,
        'page_obj':page_obj
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
    return render(request , 'posts/delete.html')

