from django.contrib import admin

from .models import Tag, PostTag

admin.site.register(Tag)
admin.site.register(PostTag)
