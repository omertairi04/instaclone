from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Posts
from .forms import PostForm

def index(request):
    search_query = ''

    if request.GET.get('search_query'): # 'search_query' emri i inputit name
        search_query = request.GET.get('search_query')

    posts = Posts.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(caption__icontains = search_query) |
        #Parentmodel__field__icontains=
        Q(owner__name__icontains=search_query)
    )

    paginator = Paginator(posts , 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts':posts,
        'paginator':paginator,
        'page_obj':page_obj,
        'search_query':search_query,
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

