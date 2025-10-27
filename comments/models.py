from django.db import models
from django.core.exceptions import ValidationError

from posts.models import Post
from users.models import Author

class Comment(models.Model):
    body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    guestname= models.CharField()
    created_at = models.DateTimeField()



