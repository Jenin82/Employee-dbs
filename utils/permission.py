from functools import wraps
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status

from utils.response import CustomResponse


def get_user_from_request(request):
    jwt_auth = JWTAuthentication()
    try:
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise ValueError("Invalid Authorization header")
        token = auth_header.split(" ")[1]
        validated_token = jwt_auth.get_validated_token(token)
        return jwt_auth.get_user(validated_token)

    except Exception as e:
        return CustomResponse(response="Error").get_failure_response(
            status_code=404, http_status_code=status.HTTP_404_NOT_FOUND
        )


def role_required(role_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            jwt_auth = JWTAuthentication()
            try:
                auth_header = request.META.get("HTTP_AUTHORIZATION")
                if not auth_header or not auth_header.startswith("Bearer "):
                    raise ValueError("Invalid Authorization header")
                token = auth_header.split(" ")[1]
                validated_token = jwt_auth.get_validated_token(token)
                user = jwt_auth.get_user(validated_token)
                try:
                    user_roles = user.role
                except AttributeError as e:
                    raise PermissionError

                if user_roles.name != role_name:
                    raise PermissionError

            except PermissionError as e:
                return CustomResponse(response="Unauthorized").get_failure_response(
                    status_code=401, http_status_code=status.HTTP_401_UNAUTHORIZED
                )
            except Exception as e:
                return CustomResponse(response=str(e)).get_failure_response(
                    status_code=401, http_status_code=status.HTTP_401_UNAUTHORIZED
                )

            return view_func(self, request, *args, **kwargs)

        return wrapper

    return decorator
