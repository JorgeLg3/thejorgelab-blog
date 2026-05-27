from django.db import models


class AboutPage(models.Model):
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="about/", blank=True, null=True)

    class Meta:
        verbose_name = "About Page"

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
