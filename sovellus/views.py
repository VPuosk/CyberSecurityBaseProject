from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import PostForm
from .forms import FilterForm

import datetime

# @login_required
def index(request):
    listPosts = Post.objects.order_by('-time')
    # template = loader.get_template('sovellus/index.html')
    context = {
        'post_list' : listPosts,
    }
    return render(request, 'sovellus/index.html', context)
    # return HttpResponse(template.render(context, request))

def showPost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post' : post,
    }
    return render(request, 'sovellus/post.html', context)

# optional filtering page (making SQL injections even easier)
def showFilteredList(request):
    if request.method == 'POST':
        form = FilterForm(request.POST)
        form.is_valid()
        filterText = form.cleaned_data['text']
        query = "SELECT * FROM sovellus_post WHERE header LIKE '%{}%'"
        query.format(filterText)
        print(query.format(filterText))
        posts = Post.objects.raw(query.format(filterText))
        context = {
            'post_list' : posts,
            'form' : form,
        }
    else:
        form = FilterForm()
        query = 'SELECT * FROM sovellus_post'
        posts = Post.objects.raw(query)
        context = {
            'post_list' : posts,
            'form' : form,
        }
    return render(request, 'sovellus/filterview.html', context)



def addNewPost(request):
    form = PostForm()
    context = {
        'form' : form,
    }
    return render(request, 'sovellus/addnew.html', context)

def postNewPost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        form.is_valid()
        formheader = form.cleaned_data['header']
        formtext = form.cleaned_data['text']
        formtime = datetime.datetime.now()
        newPost = Post(header=formheader, text=formtext, time=formtime)
        # print(form)
        newPost.save()

        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
# from django.shortcuts import render

# Create your views here.
