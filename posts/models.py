from django.db import models
from django.core.exceptions import ValidationError

from users.models import Author

class Post(models.Model):

    class PostStatus(models.TextChoices):
        DRAFT = "DRAFT"
        PUBLIC = "PUBLIC"

    title = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(choices=PostStatus, default=PostStatus.DRAFT)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def clean(self):
        super().clean()
        if self.status == self.PostStatus.DRAFT and self.published_at is not None:
            raise ValidationError({"published_at": "Draft posts cannot have a publication date."})

        if self.status == self.PostStatus.PUBLIC and self.published_at is None:
            raise ValidationError({"published_at": "Public posts must have a publication date."})

