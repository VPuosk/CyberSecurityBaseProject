from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Post
from .forms import PostForm


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
        'post' : post
    }
    return render(request, 'sovellus/post.html', context)

def addNewPost(request):
    form = PostForm()
    context = { 'form' : form }
    return render(request, 'sovellus/addnew.html', context)

def postNewPost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        print(form)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
# from django.shortcuts import render

# Create your views here.
