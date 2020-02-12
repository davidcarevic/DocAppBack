from rest_framework_simplejwt.authentication import JWTAuthentication

class UserAuthentication(JWTAuthentication):
    def authenticate(self, request):
        user = super().authenticate(request)

        try:
            token = user[1]
            request.user_meta = token.payload.get('user')
        except (KeyError, TypeError):
            request.user_meta = {}

        return user
