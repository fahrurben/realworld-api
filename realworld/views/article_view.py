from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from realworld.serializers import ArticleSerializer
from realworld.models import Article

class ArticleView(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context