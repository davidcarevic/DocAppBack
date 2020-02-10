from users.models import Users
from rest_framework_simplejwt.views import TokenObtainPairView
from users.api.serializers import UsersSerializer, MyTokenObtainPairSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from main.api.permissions import  *

class UsersViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes_by_action = {
        'create': [AllowAny],
        'list': [IsAdminUser],
        'retrieve': [AdminPermission],
        'update': [IsOwnerOrReadOnly],
        'partial_update': [IsOwnerOrReadOnly],
        'destroy': [IsOwnerOrReadOnly]
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
