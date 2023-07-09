from django.urls import path
from .views import UserCreateView, AdminDetailView

urlpatterns = [
    path('admin/', AdminDetailView.as_view(), name='admin-detail'),
    path('<str:pk>/', UserCreateView.as_view(), name='user-detail'),
    path('', UserCreateView.as_view(), name='user-list'),
]