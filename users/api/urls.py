from rest_framework import routers
from users.api.views import UsersViewSet

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')
