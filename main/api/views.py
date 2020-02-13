from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from main.models import *
from main.api.serializers import *
from main.api.permissions import *

class GenericModelViewSet(ModelViewSet):
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

class TeamsViewSet(GenericModelViewSet):
    queryset = Teams.objects.all()
    serializer_class = TeamsSerializer
    permission_classes_by_action = {}

    def list(self, request, **kwargs):
        queryset = TeamMembers.objects.filter(user_id=request.user.id)
        serializer = UsersTeamsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        queryset = TeamProjects.objects.filter(team=pk)
        serialized = TeamsProjectsSerializer(queryset, many=True)
        return Response(serialized.data)

    def create(self, request, **kwargs):
        data = request.data
        role = Roles.objects.get(name='admin')
        serialized = TeamsSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            data = {
                "user": request.user.id,
                "team": serialized.data['id'],
                "role": role.id
            }
            team_member = TeamMembersSerializer(data=data)
            if team_member.is_valid():
                team_member.save()

            return Response(serialized.data, status=201)
        else:
            return Response(serialized.errors, status=201)

class RolesViewSet(GenericModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer
    permission_classes_by_action = {}

class TeamMembersViewSet(GenericModelViewSet):
    queryset = TeamMembers.objects.all()
    serializer_class = TeamMembersSerializer
    permission_classes_by_action = {}

class ProjectsViewSet(GenericModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes_by_action = {}

    def create(self, request, **kwargs):
        description = request.data['description']
        name = request.data['name']
        team_id = request.data['teamID']
        new_data = {"name": name, "description": description}
        serialized = ProjectsSerializer(data=new_data)
        if serialized.is_valid():
            serialized.save()
            print(serialized.data["id"])
            data = {
                "project": serialized.data["id"],
                "team": team_id,
            }
            project_team = TeamProjectsSerializer(data=data)
            if project_team.is_valid():
                project_team.save()
            return Response(serialized.data, status=201)
        else:
            return Response(serialized.errors, status=201)

class TeamProjectsViewSet(GenericModelViewSet):
    queryset = TeamProjects.objects.all()
    serializer_class = TeamProjectsSerializer
    permission_classes_by_action = {}

class SectionsViewSet(GenericModelViewSet):
    queryset = Sections.objects.all()
    serializer_class = SectionsSerializer
    permission_classes_by_action = {}

class CategoriesViewSet(GenericModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes_by_action = {}

class ElementsViewSet(GenericModelViewSet):
    queryset = Elements.objects.all()
    serializer_class = ElementsSerializer
    permission_classes_by_action = {
        'partial_update': [AdminProjectLevelPermissions]
    }

class ItemsViewSet(GenericModelViewSet):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    permission_classes_by_action = {
        'partial_update': [AdminProjectLevelPermissions]
    }

class CommentsViewSet(GenericModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes_by_action = {}

class ProjectMembersViewSet(GenericModelViewSet):
    queryset = ProjectMembers.objects.all()
    serializer_class = ProjectMembersSerializer
    permission_classes_by_action = {}