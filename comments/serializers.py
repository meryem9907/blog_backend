from rest_framework import serializers

from .models import Comment
from posts.models import Post
from users.models import Author
from users.serializers import AuthorSerializer
from tags.serializers import PostSerializer

class CommentSerializer(serializers.ModelSerializer):
     post = PostSerializer(read_only=True)
     class Meta:
        model = Comment
        fields = ["id","body", "post", "guestname", "created_at"]


class CommentCreateSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ["body", "guestname", "post", "created_at"]
    
   
        
