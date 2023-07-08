from django.urls import path
from .views import UserCreateView

urlpatterns = [
    path('<str:id>/', UserCreateView.as_view(), name='user-detail'),
]