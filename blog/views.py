from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post


class PostList(ListView):
    model = Post
    template_name = "blog/post_list.html"


class PostDetail(DetailView):
    model = Post
    template_name = "blog/post_detail.html"


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/post_create.html"
    fields = ["title", "body", "tags"]

    # automatically get author from login details
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "blog/post_update.html"
    fields = ["title", "body", "tags"]

    # UserPassesTestMixin check: compares author with user
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy("home")

    # UserPassesTestMixin check: compares author with user
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user