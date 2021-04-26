from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.addNewPost, name='addNewPost'),
    path('post/<int:post_id>/', views.showPost, name='showPost'),
    path('add/new/', views.postNewPost, name='postNewPost')
]