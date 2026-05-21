from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete

urlpatterns = [
    path("new/", PostCreate.as_view(), name="post_create"),
    path("<int:pk>/", PostDetail.as_view(), name="post_detail"),
    path("<int:pk>/edit/", PostUpdate.as_view(), name="post_update"),
    path("<int:pk>/delete/", PostDelete.as_view(), name="post_delete"),
    path("", PostList.as_view(), name="post_list"),
    path("tag/<str:tag_name>", PostList.as_view(), name="post_list_tag"),
]
