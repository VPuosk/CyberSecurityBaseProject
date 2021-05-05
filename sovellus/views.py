from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver


from .models import Post
from .models import Note
from .forms import PostForm
from .forms import FilterForm

import datetime
import logging

logger = logging.getLogger(__name__)

# lets write here the logging code
# logs in failed logins
# @receiver(user_login_failed)
# def failedLogIn(sender, credentials, **kwargs):
#     logger.warning('login failed for: {credentials}'.format(
#         credentials=credentials,
#     ))

# the actual view code

@login_required
def index(request):
    listPosts = Post.objects.order_by('-time')
    # logger.info("SQL access via post list")
    context = {
        'post_list' : listPosts,
    }
    return render(request, 'sovellus/index.html', context)

def showPost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # logger.info("SQL access via show single post")
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
        # logger.warning("WARNING: Filter for SQL-RAW: {0}".format(query.format(filterText)))
        posts = Post.objects.raw(query.format(filterText))
        context = {
            'post_list' : posts,
            'form' : form,
        }
    else:
        form = FilterForm()
        # query = 'SELECT * FROM sovellus_post'
        # logger.warning("WARNING: Filter for SQL-RAW: {0}".format(query.format(filterText)))
        # posts = Post.objects.raw(query)
        context = {
            'post_list' : None,
            'form' : form,
        }
    return render(request, 'sovellus/filterview.html', context)

@login_required
def showNotes(request, name):
    # logger.info("Personal note access by {1} into notes of {0}".format(name, request.user))
    listNotes = Note.objects.filter(owner = User.objects.get(username=name)).order_by('-time')
    form = PostForm()
    context = {
        'note_list' : listNotes,
        'form' : form,
        'poster' : name
    }
    return render(request, 'sovellus/notes.html', context)

@login_required
def postNewNote(request, name):
    if request.method == 'POST':
        form = PostForm(request.POST)
        form.is_valid()
        formheader = form.cleaned_data['header']
        formtext = form.cleaned_data['text']
        formtime = datetime.datetime.now()
        formuser =  User.objects.get(username=name)
        newNote = Note(header=formheader, text=formtext, time=formtime, owner=formuser)
        newNote.save()

        return HttpResponseRedirect("/notes/{0}/".format(name))
    else:
        return HttpResponseRedirect('/')


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
        newPost.save()

        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

# from django.shortcuts import render

# Create your views here.
