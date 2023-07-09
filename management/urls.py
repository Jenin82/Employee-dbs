from django.urls import path
from .views import RoleAPIView, RoleDetailAPIView, UserCreateView, AdminDetailView

urlpatterns = [
    path('admin/', AdminDetailView.as_view(), name='admin-detail'),
    path('roles/', RoleAPIView.as_view(), name='role-list'),
    path('roles/<str:role_id>/', RoleDetailAPIView.as_view(), name='role-detail'),
    path('<str:pk>/', UserCreateView.as_view(), name='user-detail'),
    path('', UserCreateView.as_view(), name='user-list'),
]