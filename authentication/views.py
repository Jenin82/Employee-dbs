from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from utils.response import CustomResponse

class EmployeeAuthentication(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh_token = RefreshToken.for_user(user)

            token = {
                'refresh': str(refresh_token),
                'access': str(refresh_token.access_token),
            }

            return Response(token)

        return CustomResponse(response={"error": "User not found"}).get_failure_response()

