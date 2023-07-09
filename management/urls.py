from django.urls import path
from .views import UserCreateView, AdminDetailView

urlpatterns = [
    path('admin/', AdminDetailView.as_view(), name='admin-detail'),
    path('', UserCreateView.as_view(), name='user-list'),
    path('<str:id>/', UserCreateView.as_view(), name='user-detail'),
]