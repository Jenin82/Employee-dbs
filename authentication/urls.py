from django.urls import path
from authentication.views import EmployeeAuthentication

urlpatterns = [
    path('token/', EmployeeAuthentication.as_view(), name='token_obtain_pair'),
]
