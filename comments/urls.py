from django.urls import path

from .views import  CommentCreateView, CommentListView, CommentReadView, CommentDeleteView

urlpatterns = [
    path("create/<int:post_id>/", CommentCreateView.as_view(), name="create_comment"),
    path("delete/<int:pk>/", CommentDeleteView.as_view(), name="delete_comment"),
    path("read/<int:pk>/", CommentReadView.as_view(), name="read_comment"),
    path("list/<int:post_id>/", CommentListView.as_view(), name="list_comment"),
]