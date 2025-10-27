from django.urls import path

from .views import PostListView, PostReadView, PostCreateView, PostDeleteView, PostUpdateView

urlpatterns = [
    path("create/", PostCreateView.as_view(), name="create_post"),
    path("update/<int:pk>/", PostUpdateView.as_view(), name="update_post"),
    path("delete/<int:pk>/", PostDeleteView.as_view(), name="delete_post"),
    path("read/<int:pk>/", PostReadView.as_view(), name="read_post"),
    path("list/", PostListView.as_view(), name="list_posts")
]