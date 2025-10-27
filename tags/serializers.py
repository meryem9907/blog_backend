from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


from .models import Tag, PostTag
from posts.models import Post

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id","title", "body", "updated_at", "published_at", "status", "author", "created_at"]

class PostTagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = []
        
class TagCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Tag
            fields = ["name", "slug"]
    
class PostTagDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class PostTagReadSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta: 
        model = PostTag
        fields = ["id","tag", "post"]
        read_only_fields = fields

class TagReadSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Tag
        fields = ["id","name", "slug"]
        read_only_fields = fields