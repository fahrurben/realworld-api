from rest_framework.views import APIView, Response, status
from django.http import JsonResponse

from realworld.serializers import CommentSerializer
from realworld.models import Article, Comment

class CommentDetailsView(APIView):

    def delete(self, request, slug, pk):
        article = Article.objects.filter(slug=slug).first()
        comment = Comment.objects.filter(pk=pk).first()

        if article is None or comment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_authenticated or not comment.author == request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
