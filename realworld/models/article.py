from django.db import models
from django.utils.text import slugify

from .custom_user import CustomUser
from .tag import Tag

class Article(models.Model):
    slug = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    @property
    def favorited(self):
        return self.favorites_by.exists()

    @property
    def favorites_count(self):
        return self.favorites_by.count()
