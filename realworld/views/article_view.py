from rest_framework import viewsets
from rest_framework.views import Response, status
from django.db.models import Q

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

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        offset = int(self.request.query_params.get('offset', 0))
        limit = int(self.request.query_params.get('limit', 20))
        tag = self.request.query_params.get('tag')
        author = self.request.query_params.get('author')
        favorited = self.request.query_params.get('favorited')

        q = ~Q(pk__in=[])
        if tag:
            q &= Q(tags__name=tag)

        if author:
            q &= Q(author__username=author)

        if favorited:
            q &= Q(favorites_by__username=favorited)

        queryset = Article.objects.filter(q).order_by('-created_at').all()[offset:offset+limit]
        serializer = ArticleSerializer(queryset, many=True)
        return Response({
            'articles': serializer.data
        })