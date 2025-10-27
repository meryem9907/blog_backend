from rest_framework import serializers

from .models import Post
from users.serializers import AuthorSerializer

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "body", "created_at", "updated_at", "published_at", "status"] # author is added in view as request.user
        
    def validate(self, data):
        instance = Post(**data)
        instance.clean() # here it is called on purpose so that the dates are validated
        return data
    
class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id","title", "body", "updated_at", "published_at", "status"] 
        read_only_fields = ["author", "created_at"] # author and created_at should not be changed

class PostDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PostReadSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ["id","title", "body", "updated_at", "published_at", "status", "author", "created_at"]
        read_only_fields = fields

