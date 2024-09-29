from django.contrib import admin

# Register your models here.
from realworld.models import CustomUser, Article, Tag

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Article)
admin.site.register(Tag)