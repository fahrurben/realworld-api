from rest_framework.views import APIView, Response, status
from django.http import JsonResponse

from realworld.serializers import CommentSerializer
from realworld.models import Article, Comment

class CommentListView(APIView):

    def post(self, request, slug):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        article = Article.objects.get(slug=slug)
        serializer = CommentSerializer(data=request.data, context={'request': request, 'article_id': article.id})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

    def get(self, request, slug):
        article = Article.objects.get(slug=slug)
        serializer = CommentSerializer(article.comments.all(), many=True)
        return Response({'comments': serializer.data}, status=status.HTTP_200_OK)

