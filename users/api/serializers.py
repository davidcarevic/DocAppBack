from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer
from users.models import Users, EmailInvitation, PasswordReset
from main.models import ProjectMembers

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

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        try:
            instance.set_password(validated_data['password'])
            instance.save()
        except:
            pass

        return instance

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        projects = ProjectMembers.objects.filter(user=user.id)
        project_access = {}
        for p in projects:
            project_access[str(p.project.id)] = p.role.id
        token = super().get_token(user)
        token['user'] = {
            'id': user.id,
            'email': user.email,
            'data': user.data,
            'project_access': project_access,
        }
        return token

class EmailInvitationSerializer(ModelSerializer):
    class Meta:
        model = EmailInvitation
        fields = '__all__'
        read_only_fields = ['pk', 'created_at', 'updated_at']

class PasswordResetSerializer(ModelSerializer):
    class Meta:
        model = PasswordReset
        fields = '__all__'
        read_only_fields = ['pk', 'created_at', 'updated_at']