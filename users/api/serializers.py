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
