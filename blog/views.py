from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


class PostList(ListView):
    model = Post
    template_name = "blog/post_list.html"


class PostDetail(DetailView):
    model = Post
    template_name = "blog/post_detail.html"