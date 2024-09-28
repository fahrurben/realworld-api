from rest_framework.views import APIView, Response, status

from realworld.models import CustomUser
from realworld.serializers import ProfileSerializer

class ProfileView(APIView):

    def get(self, request, username):
        logged_in_user = request.user

        user = CustomUser.objects.filter(username=username).first()
        if user is not None:
            profile_serializer = ProfileSerializer(user)
            profile_serializer.data['profile']['following'] = False

            if logged_in_user.is_authenticated:
                if logged_in_user.follows.filter(username=user.username).exists():
                    profile_serializer.data['profile']['following'] = True

            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'username is not found',
            }, status=status.HTTP_404_NOT_FOUND)



