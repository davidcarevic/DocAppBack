from django.contrib import admin
from rest_framework import routers
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view
from users.api.urls import router as users_router
from main.api.urls import router as main_router
from users.api.views import MyTokenObtainPairView
from rest_framework_simplejwt import views as jwt_views

schema_view = get_swagger_view(title='Knowledge Base App API')
router = routers.DefaultRouter()
router.registry.extend(users_router.registry)
router.registry.extend(main_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('doc/', schema_view),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
