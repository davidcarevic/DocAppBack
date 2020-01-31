from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer
from users.models import Users

#Main Category Serializer
class UsersSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        read_only_fields = ['pk', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        token['email'] = user.email
        token['data'] = user.data
        return token
