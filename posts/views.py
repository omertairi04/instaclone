from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse

from .models import Posts , Likes , Comment
from .forms import PostForm , CommentForm

def index(request):
    user = request.user.profile
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
        'user':user,
        'posts':posts,
        'paginator':paginator,
        'page_obj':page_obj,
        'search_query':search_query,
    }
    return render(request , 'index.html',context)

def like(request , pk ):
    user = request.user
    post = Posts.objects.get(id=pk)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user , post=post).count()
    if not liked:
        liked = Likes.objects.create(user=user , post=post)
        current_likes = current_likes + 1
    else:
        liked = Likes.objects.filter(user=user , post=post).delete()
        current_likes = current_likes - 1
    post.likes = current_likes
    post.save()

    next = request.GET.get('next' , '/')

    return redirect(next)


def singlePost(request , pk):
    post = Posts.objects.get(id=pk)
    comments = post.comment_set.all()
    commentForm = CommentForm()

    if request.method == 'POST':
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            comment = commentForm.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()

        return redirect('singlePost' , pk=post.id)

    context = {
        'post':post,
        'comments':comments,
        'commentForm':commentForm
    }
    return render(request,'posts/singelPost.html',context)

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

