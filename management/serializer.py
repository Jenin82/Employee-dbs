from rest_framework import serializers
from authentication.models import DepartmentUserLink, Role, User

class UserDepartmentSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    role_name = serializers.SerializerMethodField()

    def get_department(self, user):
        try:
            department_user_link = DepartmentUserLink.objects.get(user_id=user.id)
            return {
                "id": department_user_link.department.id,
                "title": department_user_link.department.title,
            }
        except DepartmentUserLink.DoesNotExist:
            return None

    def get_role_name(self, user):
        role = user.role
        return role.name if role else None

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
            "role",
            "role_name",
        ]


class RoleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Role
        fields = ['id', 'name']