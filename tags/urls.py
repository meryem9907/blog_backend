from django.urls import path

from .views import PostTagCreateView, PostTagDeleteView, TagReadView, PostTagListView,TagCreateView, TagListView

urlpatterns = [
    path("create/", TagCreateView.as_view(), name="create_tag"),
    path("create/tag/<int:tag_id>/post/<int:post_id>/", PostTagCreateView.as_view(), name="create_post_tag"),
    path("delete/<int:tag_id>/", PostTagDeleteView.as_view(), name="delete_tag"),
    path("read/<int:tag_id>/", TagReadView.as_view(), name="read_tag"),
    path("list/post-tags/<int:post_id>/", PostTagListView.as_view(), name="list_post_tag"),
    path("list/", TagListView.as_view(), name="list_tags")
]
