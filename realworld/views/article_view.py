from rest_framework import viewsets
from rest_framework.views import Response, status
from rest_framework.decorators import action
from django.db.models import Q
from django.http import JsonResponse

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
        queryCount = Article.objects.filter(q).count()
        serializer = ArticleSerializer(queryset, many=True)
        return Response({
            'articles': serializer.data,
            'articlesCount': queryCount,
        })

    @action(detail=False)
    def feed(self, request):
        offset = int(self.request.query_params.get('offset', 0))
        limit = int(self.request.query_params.get('limit', 20))

        follows = request.user.follows.all()

        q = Q(author__in=follows)

        queryset = Article.objects.filter(q).order_by('-created_at').all()[offset:offset + limit]
        queryCount = Article.objects.filter(q).count()

        serializer = ArticleSerializer(queryset, many=True)
        return Response({
            'articles': serializer.data,
            'articlesCount': queryCount,
        })

    @action(detail=True, methods=['POST'], name='favorite_article')
    def favorite(self, request, slug):
        current_user = request.user
        article = Article.objects.filter(slug=slug).first()

        if article is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        current_user.favorite_articles.add(article)
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data, status=201)

    @favorite.mapping.delete
    def unfavorite(self, request, slug):
        current_user = request.user
        article = Article.objects.filter(slug=slug).first()

        if article is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        current_user.favorite_articles.remove(article)
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data, status=201)