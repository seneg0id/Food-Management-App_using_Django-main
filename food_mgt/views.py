# from django.shortcuts import render
# from .models import Post
from difflib import context_diff
from msilib.schema import ListView
from operator import truediv
from urllib import request
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.views.generic import (ListView, DetailView,CreateView,UpdateView,DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import statusupdate

# Create your views here.

def open(request):
    return render(request,'food_mgt/open.html')

    
def home(request):
    context = {
        'test1' : Post.objects.all(),
        'place' : 0

    }
    return render(request,'food_mgt/home.html',context)

def search(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    items = Post.objects.filter(city__icontains=q)
    context = {
        'test1' : items,
        'place' : 1
    }

    return render(request,'food_mgt/home.html',context)



def food(request,id):
    username = ''
    if request.user.is_authenticated:
        username = request.user.username

    member = Post.objects.get(id = id)
    member.status = 'Booked'
    member.booked = username
    member.save()
    return redirect('requested-orders')

def cancel(request,id):
    member = Post.objects.get(id = id)
    member.status = 'Available'
    member.booked = ''
    member.save()
    return redirect('blog-home')

def requested(request):
    username =''
    if request.user.is_authenticated:
        username = request.user.username
    
    context = {
        'test2' : Post.objects.all(),
        'name' : username
    }
    
    return render(request,'food_mgt/requested.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'food_mgt/home.html'
    context_object_name = 'test1'
    ordering = ['-date_posted']
    paginate_by = 5

   
class UserPostListView(ListView):
    model = Post
    template_name = 'food_mgt/user_posts.html'
    context_object_name = 'test2'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin,CreateView):
    # The CreateView page displayed to a GET request uses a template_name_suffix of '_form'
    model = Post
    fields = ['title', 'content','contact_name','contact_number','date','state','city','image']

    def form_valid(self,form):   # when used this function it fills the author instance of the form and retunrs the valid data and django saves it
                                 # we should only use form_valid as the name of the function 
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title', 'content','contact_name','contact_number','date','state','city','image','status']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super(PostUpdateView,self).form_valid(form)


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url='/home'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'food_mgt/about.html', {'title' : 'ABOUT'})


