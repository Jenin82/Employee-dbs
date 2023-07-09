# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserSerializer, UserDepartmentSerializer
from rest_framework.permissions import IsAuthenticated
from utils.permission import role_required
from utils.types import RoleType
from rest_framework import status
from authentication.models import User, DepartmentUserLink
from utils.response import CustomResponse


class UserCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @role_required(RoleType.ADMIN.value)
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
            serializer = UserSerializer(user)
        else:
            # List all users with their departments
            users = User.objects.prefetch_related(
                "departmentuserlink_set__department"
            ).all()
            serializer = UserDepartmentSerializer(users, many=True)
        return CustomResponse(response=serializer.data).get_success_response()

    @role_required(RoleType.ADMIN.value)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return CustomResponse(
                response="User created successfully", message=serializer.data
            ).get_success_response()

        return CustomResponse(response=serializer.errors).get_failure_response()

    @role_required(RoleType.ADMIN.value)
    def patch(self, request, pk=None):
        if pk is not None:
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = UserSerializer(user, data=request.data, partial=True)
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

    @role_required(RoleType.ADMIN.value)
    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return CustomResponse(
                response={"error": "User not found"}
            ).get_failure_response()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
