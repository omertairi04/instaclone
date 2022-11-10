from django.urls import path

from . import views

urlpatterns = [
    path('',views.index , name='index'),
    path('post/<str:pk>/',views.singlePost , name='singlePost'),
    path('<str:pk>/like/',views.like , name='like'),

    path('create/',views.createPost , name='create'),
    path('edit/<str:pk>/',views.editPost , name='edit'),
    path('delete/<str:pk>/',views.deletePost , name='delete'),
]

