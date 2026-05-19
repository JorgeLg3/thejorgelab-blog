from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("health/", include("healthcheck.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("posts/", include("blog.urls")),
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
]
