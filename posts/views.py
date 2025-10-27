from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404

from .serializers import PostCreateSerializer, PostUpdateSerializer, PostDeleteSerializer, PostReadSerializer
from .models import Post

class PostCreateView(generics.CreateAPIView):
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated] 

    def perform_create(self, serializer):
            serializer.save(author=self.request.user)

class PostUpdateView(generics.UpdateAPIView):
    serializer_class = PostUpdateSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

class PostDeleteView(generics.DestroyAPIView):
    serializer_class = PostDeleteSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

class PostReadView(generics.RetrieveAPIView):
    serializer_class = PostReadSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

class PostListView(generics.ListAPIView):
    serializer_class = PostReadSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]