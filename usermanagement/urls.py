from django.urls import path
from .views import *

urlpatterns = [
    path('signup', SignUpUserAPIView.as_view(), name='signup'),
    path('UserLogin', UserLoginApiView.as_view(), name='UserLogin'),
]
