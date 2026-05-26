from django.db.models import Count
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post, Tag
from .forms import PostForm


class PostList(ListView):
    model = Post
    template_name = "blog/post_list.html"

    def get_queryset(self):
        queryset = Post.objects.order_by("-date")  # type: ignore
        tag_name = self.kwargs.get("tag_name")
        if tag_name:
            return queryset.filter(tags__name=tag_name)
        return queryset.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_tags"] = (
            Tag.objects.annotate(post_count=Count("posts"))  # type: ignore
            .filter(post_count__gt=0)
            .order_by("-post_count")[:10]
        )
        context["recent_posts"] = Post.objects.order_by("-date")[:3]  # type: ignore
        context["current_tag"] = self.kwargs.get("tag_name")
        return context


class PostDetail(DetailView):
    model = Post
    template_name = "blog/post_detail.html"


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/post_create.html"
    form_class = PostForm

    def form_valid(self, form):
        # automatically get author from login details
        form.instance.author = self.request.user
        response = super().form_valid(form)

        # Process list of tags
        tag_list = form.cleaned_data["tag_list"]

        for tag_name in tag_list.split():
            tag_name = tag_name.lower().strip()

            if tag_name:
                tag, created = Tag.objects.get_or_create(name=tag_name)  # type: ignore
                self.object.tags.add(tag)  # type: ignore

        return response

    # On preview load the body content into the preview variable
    def post(self, request, *args, **kwargs):
        self.object = None

        form = self.get_form()

        if form.is_valid():
            if "preview" in request.POST:
                return self.render_to_response(
                    self.get_context_data(
                        form=form,
                        preview=form.cleaned_data["body"],
                    )
                )

            return self.form_valid(form)

        return self.form_invalid(form)


class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "blog/post_update.html"
    form_class = PostForm

    # UserPassesTestMixin check: compares author with user
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    # Include current tags in the tag list
    def get_initial(self):
        initial = super().get_initial()

        initial["tag_list"] = " ".join(tag.name for tag in self.object.tags.all())

        return initial

    # update tags from tag list
    def form_valid(self, form):
        response = super().form_valid(form)

        tag_list = form.cleaned_data["tag_list"]

        # remove existing relations first
        self.object.tags.clear()

        for tag_name in tag_list.split():
            tag_name = tag_name.lower().strip()

            if tag_name:
                tag, created = Tag.objects.get_or_create(name=tag_name)  # type: ignore
                self.object.tags.add(tag)

        return response


class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy("home")

    # UserPassesTestMixin check: compares author with user
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
