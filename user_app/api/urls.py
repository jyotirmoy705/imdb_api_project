from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import RegistrationView,LogoutView


urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('registration/', RegistrationView, name='registration'),
    path('logout/', LogoutView, name='logout'),
]
