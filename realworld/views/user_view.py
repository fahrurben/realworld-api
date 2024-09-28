from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from realworld.models import CustomUser
from realworld.serializers import RegisterSerializer, UserSerializer

class UserView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = CustomUser.objects.create_user(username, email, password)
            refresh = RefreshToken.for_user(user)

            user_serializer = UserSerializer(user)
            user_serializer.data['user']['token'] = str(refresh.access_token)

            return Response(user_serializer.data,  status=status.HTTP_200_OK)
        else:
            return Response({
                'message': serializer.errors,
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        user_serializer = UserSerializer(request.user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        if not request.user.is_authenticated:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        user = request.user
        serializer = UserSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            if 'password' in serializer.validated_data:
                user.set_password(serializer.validated_data.pop('password'))

            user.__dict__.update(serializer.validated_data)

            user.save()

            user_serializer = UserSerializer(request.user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': serializer.errors,
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)