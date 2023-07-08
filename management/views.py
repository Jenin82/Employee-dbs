
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserSerializer
from rest_framework.permissions import IsAuthenticated
from utils.permission import role_required
from utils.types import RoleType

class UserCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    @role_required(RoleType.ADMIN.value)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
