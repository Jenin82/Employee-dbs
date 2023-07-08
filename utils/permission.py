from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.response import Response
from typing import Any, Dict, List
import inspect
from rest_framework import authentication



class CustomResponse:
    """A custom response class for API views.

    Attributes:
        message (Dict[str, Any]): A dictionary of messages.
        response (Dict[str, Any]): A dictionary of response data.
    """

    def __init__(
        self,
        message: Dict[str, Any] = None,
        general_message: List[str] = None,
        response: Dict[str, Any] = None,
    ) -> None:
        """Initializes the CustomResponse object.

        Args:
            message (Dict[str, Any], optional): A dictionary of messages.
                Defaults to {}.
            general_message (List[str], optional): A list of general messages.
                Defaults to [].
            response (Dict[str, Any], optional): A dictionary of response data.
                Defaults to {}.
        """
        self.message = {} if message is None else message
        self.general_message = [] if general_message is None else general_message
        self.response = {} if response is None else response

        if not isinstance(self.general_message, list):
            self.general_message = [self.general_message]

        self.message = {"general": self.general_message} | self.message
        

    def get_success_response(self) -> Response:
        """Returns a success response.

        Returns:
            Response: A success response object.
        """
        return Response(
            data={
                "hasError": False,
                "statusCode": status.HTTP_200_OK,
                "message": self.message,
                "response": self.response,
            },
            status=status.HTTP_200_OK,
        )

    def get_failure_response(
        self,
        status_code: int = 400,
        http_status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> Response:
        """Returns a failure response.

        Args:
            status_code (int, optional): A custom status code for the response.
                Defaults to 400.
            http_status_code (int, optional): An HTTP status code for the response.
                Defaults to status.HTTP_400_BAD_REQUEST.

        Returns:
            Response: A failure response object.
        """
        return Response(
            data={
                "hasError": True,
                "statusCode": status_code,
                "message": self.message,
                "response": self.response,
            },
            status=http_status_code,
        )

    def paginated_response(self, data: dict, pagination: dict) -> Response:
        """
        Generates a paginated response.

        Args:
            data (dict): The data to be included in the response.
            pagination (dict): The pagination details.

        Returns:
            Response: The generated paginated response.

        """

        self.response.update({"data": data, "pagination": pagination})
        return Response(
            data={
                "hasError": False,
                "statusCode": status.HTTP_200_OK,
                "message": self.message,
                "response": self.response,
            },
            status=status.HTTP_200_OK,
        )

def role_required(role_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            # Verify JWT token and extract roles
            jwt_auth = JWTAuthentication()
            try:
                auth_header = request.META.get('HTTP_AUTHORIZATION')
                if not auth_header or not auth_header.startswith('Bearer '):
                    raise ValueError("Invalid Authorization header")
                token = auth_header.split(' ')[1]
                validated_token = jwt_auth.get_validated_token(token)
                user = jwt_auth.get_user(validated_token)
                user_roles = user.role
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if user_roles.name != role_name:
                return Response(
                    {"error": "Unauthorized"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            return view_func(self, request, *args, **kwargs)
        return wrapper
    return decorator