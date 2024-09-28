from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.tokens import RefreshToken

from realworld.serializers import LoginSerializer
from realworld.models import CustomUser

class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = CustomUser.objects.filter(email=email).first()
            if user is None:
                return Response({'message': 'email or password is wrong'}, status=status.HTTP_400_BAD_REQUEST)
            if not user.check_password(password):
                return Response({'message': 'email or password is wrong'}, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },  status=status.HTTP_200_OK)
