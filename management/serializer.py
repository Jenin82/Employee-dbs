from rest_framework import serializers
from authentication.models import DepartmentUserLink, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "mobile",
            "gender",
            "dob",
            "role",
        ]


class UserDepartmentSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()

    def get_department(self, user):
        try:
            department_user_link = DepartmentUserLink.objects.get(user_id=user.id)
            return {
                "id": department_user_link.department.id,
                "title": department_user_link.department.title,
            }
        except DepartmentUserLink.DoesNotExist:
            return None

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "mobile",
            "gender",
            "dob",
            "created_at",
            "department",
        ]
