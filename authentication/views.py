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

            access_token = str(refresh_token.access_token)
            refresh_token = str(refresh_token)

            token_data = {
                'refresh': refresh_token,
                'access': access_token,
            }

            return CustomResponse(response=token_data).get_success_response()

        return CustomResponse(response={"error": "Invalid Username or password"}).get_failure_response()

