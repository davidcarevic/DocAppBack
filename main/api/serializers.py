
from rest_framework.serializers import ModelSerializer
from main.models import *
from users.api.serializers import UsersSerializer

class TeamsSerializer(ModelSerializer):
    class Meta:
        model = Teams
        fields = '__all__'
        read_only_fields = ['pk', 'created_at', 'updated_at']

class RolesSerializer(ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'
        read_only_fields = ['pk', 'created_at', 'updated_at']

class TeamMembersSerializer(ModelSerializer):
    class Meta:
        model = TeamMembers
        fields = '__all__'
        read_only_fields = ['pk', 'created_at', 'updated_at']

class ProjectsSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'
        read_only_fields = ['pk', 'created_at', 'updated_at']

class TeamProjectsSerializer(ModelSerializer):
    class Meta:
        model = TeamProjects
        fields = '__all__'
        read_only_fields = ['pk', 'created_at', 'updated_at']

class SectionsSerializer(ModelSerializer):
    class Meta:
        model = Sections
        fields = '__all__'
        read_only_fields = ['pk', 'created_at', 'updated_at']

class CategoriesSerializer(ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'
        read_only_fields = ['pk', 'created_at', 'updated_at']

class ElementsSerializer(ModelSerializer):
    class Meta:
        model = Elements
        fields = '__all__'
        read_only_fields = ['pk', 'created_at', 'updated_at']

class ItemsSerializer(ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'
        read_only_fields = ['pk', 'created_at', 'updated_at']

class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ['pk', 'created_at', 'updated_at']
