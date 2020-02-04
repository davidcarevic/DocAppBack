from users.models import Users
from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt

class UserAuthentication(JWTAuthentication):
    def authenticate(self, request):
        user = super().authenticate(request)
        token = user[1]
        request.user_meta = token.payload.get('user')

        return user
