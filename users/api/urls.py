from rest_framework import routers
from users.api.views import UsersViewSet, EmailInvitationViewSet

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register('email-invitations', EmailInvitationViewSet, basename='eamil-invitation')
