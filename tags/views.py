from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.http import HttpResponse

from .serializers import PostTagCreateSerializer, PostTagDeleteSerializer, PostTagReadSerializer, TagCreateSerializer, TagReadSerializer
from .models import PostTag,Tag
from posts.models import Post

class TagCreateView(generics.CreateAPIView):
    serializer_class=TagCreateSerializer
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated]

class PostTagCreateView(generics.CreateAPIView):
    serializer_class = PostTagCreateSerializer
    queryset = queryset = PostTag.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        tag =  get_object_or_404(Tag,  id=self.kwargs["tag_id"])
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        if PostTag.objects.filter(post=post, tag=tag).exists():            
            raise ValidationError("This post already has that tag.")
        serializer.save(post=post, tag=tag)

class PostTagDeleteView(generics.DestroyAPIView):
    serializer_class = PostTagDeleteSerializer
    permission_classes = [IsAuthenticated]
    queryset = Tag.objects.all()
    
    def get_object(self):
        return get_object_or_404(
            Tag,
            id=self.kwargs["tag_id"],
        )

class TagReadView(generics.RetrieveAPIView):
    serializer_class = TagReadSerializer
    queryset = Tag.objects.all()
    permission_classes = [AllowAny]

    def get_object(self):
        return get_object_or_404(Tag,id=self.kwargs["tag_id"] )
    
class TagListView(generics.ListAPIView):
    serializer_class = TagReadSerializer
    permission_classes = [AllowAny]
    queryset = Tag.objects.all()

   

class PostTagListView(generics.ListAPIView):
    serializer_class = PostTagReadSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        post_tag = PostTag.objects.filter(post=post).select_related("tag", "post")
        return post_tag
    