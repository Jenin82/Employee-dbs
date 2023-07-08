from django.urls import path
from .views import UserCreateView

urlpatterns = [
    path('', UserCreateView.as_view(), name='user-list'),
    path('<str:id>/', UserCreateView.as_view(), name='user-detail'),
]