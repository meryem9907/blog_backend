from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from .serializers import CommentCreateSerializer, CommentSerializer
from .models import Comment
from posts.models import Post

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [AllowAny]
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        serializer.save(post=post)

class CommentDeleteView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()

    def get_object(self):
        return get_object_or_404(
            Comment,
            id=self.kwargs["pk"],
        )

class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    queryset = Comment.objects.all()

    def get_queryset(self):
        comments = Comment.objects.filter(post=self.kwargs["post_id"])
        return comments

class CommentReadView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    queryset = Comment.objects.all()

    def get_object(self):
        comments = get_object_or_404(Comment, id=self.kwargs["pk"])
        return comments