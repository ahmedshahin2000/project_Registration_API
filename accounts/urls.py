from django.urls import path, include
from .views import (ClientSignupView, CustomAuthToken, LogoutView) #ChangePasswordView

urlpatterns = [
    path('signup/client/', ClientSignupView.as_view()),
    path('login/', CustomAuthToken.as_view(), name='auth_token'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    # path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]