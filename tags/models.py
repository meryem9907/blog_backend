from django.db import models
from django.core.exceptions import ValidationError

from posts.models import Post

class Tag(models.Model):
    name = models.CharField()
    slug = models.CharField(unique=True)

class PostTag(models.Model):
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE, related_name="tags")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="posts")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["post","tag"], name="uniq_post_tag")]

