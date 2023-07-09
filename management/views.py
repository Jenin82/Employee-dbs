# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import RoleSerializer, UserDepartmentSerializer
from rest_framework.permissions import IsAuthenticated
from utils.permission import get_user_from_request, role_required
from utils.types import RoleType
from rest_framework import status
from authentication.models import Role, User, DepartmentUserLink
from utils.response import CustomResponse


class UserCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is not None:
            try:
                user = User.objects.prefetch_related(
                    "departmentuserlink_set__department"
                ).get(pk=pk)
            except User.DoesNotExist:
                return CustomResponse(
                    response={"error": "User not found"}
                ).get_failure_response()
            serializer = UserDepartmentSerializer(user)
        else:
            users = User.objects.prefetch_related(
                "departmentuserlink_set__department"
            ).all()
            serializer = UserDepartmentSerializer(users, many=True)
        return CustomResponse(response=serializer.data).get_success_response()

    @role_required(RoleType.MANAGER.value)
    def post(self, request):
        serializer = UserDepartmentSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return CustomResponse(
                response="User created successfully", message=serializer.data
            ).get_success_response()

        return CustomResponse(response=serializer.errors).get_failure_response()

    @role_required(RoleType.MANAGER.value)
    def patch(self, request, pk=None):
        if pk is not None:
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = UserDepartmentSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse(response=serializer.data).get_success_response()
            return CustomResponse(response=serializer.errors).get_failure_response()

        else:
            department_id = request.data.get("department_id")
            user_id = request.data.get("user_id")

            try:
                department_user_link = DepartmentUserLink.objects.get(user_id=user_id)
            except DepartmentUserLink.DoesNotExist:
                return CustomResponse(
                    response={"error": "Department-User link not found"}
                ).get_failure_response()
            department_user_link.department_id = department_id
            department_user_link.save()
            return CustomResponse(
                response={"message": "Department updated successfully"}
            ).get_success_response()

    @role_required(RoleType.MANAGER.value)
    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return CustomResponse(
                response={"error": "User not found"}
            ).get_failure_response()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @role_required(RoleType.MANAGER.value)
    def get(self, request):
        try:
            user = get_user_from_request(request)
            serializer = UserDepartmentSerializer(user)
            return CustomResponse(response=serializer.data).get_success_response()
        except User.DoesNotExist:
            return CustomResponse(
                response={"error": "User not found"}
            ).get_failure_response()
            
            
class RoleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @role_required(RoleType.MANAGER.value)
    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        response = CustomResponse(response=serializer.data)
        return response.get_success_response()
    
    @role_required(RoleType.MANAGER.value)
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = CustomResponse(response=serializer.data)
            return response.get_success_response()
        response = CustomResponse(message=serializer.errors)
        return response.get_failure_response()

class RoleDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @role_required(RoleType.MANAGER.value)
    def get_object(self, role_id):
        try:
            return Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return None
        
    @role_required(RoleType.MANAGER.value)
    def get(self, request, role_id):
        if role := self.get_object(role_id):
            serializer = RoleSerializer(role)
            response = CustomResponse(response=serializer.data)
            return response.get_success_response()
        response = CustomResponse(
            general_message=["Role does not exist."]
        )
        return response.get_failure_response(status_code=404, http_status_code=status.HTTP_404_NOT_FOUND)
    
    @role_required(RoleType.MANAGER.value)
    def put(self, request, role_id):
        if role := self.get_object(role_id):
            serializer = RoleSerializer(role, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = CustomResponse(response=serializer.data)
                return response.get_success_response()
            response = CustomResponse(message=serializer.errors)
            return response.get_failure_response()
        response = CustomResponse(
            general_message=["Role does not exist."]
        )
        return response.get_failure_response(status_code=404, http_status_code=status.HTTP_404_NOT_FOUND)
    
    @role_required(RoleType.MANAGER.value)
    def delete(self, request, role_id):
        if role := self.get_object(role_id):
            role.delete()
            response = CustomResponse()
            return response.get_success_response()
        response = CustomResponse(
            general_message=["Role does not exist."]
        )
        return response.get_failure_response(status_code=404, http_status_code=status.HTTP_404_NOT_FOUND)