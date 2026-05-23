from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tag_detail", kwargs={"pk": self.pk})


class Post(models.Model):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))
        
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="posts/", blank=True, null=True, validators=[validate_image])
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
    
