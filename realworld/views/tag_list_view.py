from rest_framework.views import APIView, Response, status
from django.http import JsonResponse

from realworld.models import Tag

class TagListView(APIView):
    def get(self, request):
        tags = Tag.objects.values_list('name', flat=True)
        return JsonResponse({'tags': list(tags)}, status=status.HTTP_200_OK)