from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from blog.views import PostList

urlpatterns = [
    path("health/", include("healthcheck.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", PostList.as_view(), name="home"),
    path("tag/<str:tag_name>", PostList.as_view(), name="post_list_tag"),
    path("posts/", RedirectView.as_view(pattern_name="home", permanent=True)),
    path("posts/", include("blog.urls")),
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
