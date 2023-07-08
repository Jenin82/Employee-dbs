from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class EmployeeAuthentication(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Perform authentication
        user = authenticate(request, username=username, password=password)

        if user is not None:
            serializer = TokenObtainPairSerializer(data={'username': username, 'password': password})
            serializer.is_valid(raise_exception=True)
            refresh_token = RefreshToken.for_user(user)
            token = {
                'refresh': str(refresh_token),
                'access': str(refresh_token.access_token),
            }
            return Response(token)
        
        # Handle invalid credentials
        return Response({'error': 'Invalid credentials'}, status=400)
