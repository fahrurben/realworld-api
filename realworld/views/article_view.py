from rest_framework import viewsets

from realworld.serializers import ArticleSerializer
from realworld.models import Article
from realworld.permissions import AuthorUpdatePermission

class ArticleView(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'slug'
    permission_classes = [AuthorUpdatePermission]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context