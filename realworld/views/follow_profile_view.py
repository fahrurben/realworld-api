from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated

from realworld.models import CustomUser
from realworld.serializers import ProfileSerializer

class FollowProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        logged_in_user = request.user

        user = CustomUser.objects.filter(username=username).first()
        if user is not None:
            logged_in_user.follows.add(user)
            profile_serializer = ProfileSerializer(user, context={'request': request})
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'username is not found',
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, username):
        logged_in_user = request.user

        user = CustomUser.objects.filter(username=username).first()
        if user is not None:
            logged_in_user.follows.remove(user)
            profile_serializer = ProfileSerializer(user, context={'request': request})
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'username is not found',
            }, status=status.HTTP_404_NOT_FOUND)
