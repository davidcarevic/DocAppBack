from rest_framework import routers
from users.api.views import UsersViewSet, EmailInvitationViewSet, PasswordResetViewSet

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register('email-invitations', EmailInvitationViewSet, basename='eamil-invitation')
router.register('password-reset', PasswordResetViewSet, basename='password-reset')
