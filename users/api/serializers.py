from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer
from users.models import Users
from main.api.serializers import UsersTeamsPKSerializer
from main.models import TeamMembers

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
        team = TeamMembers.objects.filter(user=user.id)
        teams = UsersTeamsPKSerializer(team, many=True)
        token = super().get_token(user)
        token['user'] = {
            'id': user.id,
            'email': user.email,
            'data': user.data,
            'teams': teams.data
        }
        return token
