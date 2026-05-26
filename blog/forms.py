from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    tag_list = forms.CharField(
        required=False,
        help_text="Write tags separated by spaces, for example: django python webdev",
    )

    class Meta:
        model = Post
        fields = ["title", "body", "image", "tag_list", "featured"]
        # widgets = {"tags": forms.widgets.CheckboxSelectMultiple()}
