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
        user_id = request.user_meta['id']
        data = request.data
        new_data = {
            'name': data['name'],
            'description': data['description'],
            'data': {
                'image': data['image']
            }
        }
        serialized = ProjectsSerializer(data=new_data)
        if serialized.is_valid():

            serialized.save()
            data = {
                "project": serialized.data["id"],
                "user": user_id,
                "role": 0
            }
            project_user = ProjectMembersSerializer(data=data)
            if project_user.is_valid():
                project_user.save()
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


# returns all projects for a user
class UsersProjectViewSet(ViewSet):
    def list(self, request, **kwargs):
        queryset = ProjectMembers.objects.filter(user_id=request.user.id)
        serializer = UsersProjectsSerializer(queryset, many=True)
        return Response(serializer.data)


class ProjectSectionsView(ViewSet):
    def retrieve(self, request, pk=None, **kwargs):
        queryset = Sections.objects.filter(project=pk)
        serializer = SectionsSerializer(queryset, many=True)
        return Response(serializer.data)


class SectionCategoriesView(ViewSet):
    def retrieve(self, request, pk=None, **kwars):
        queryset = Categories.objects.filter(section=pk).order_by('id')
        serializer = CategoryElementsSerializer(queryset, many=True)
        return Response(serializer.data)


class CategoryElementsView(ViewSet):
    permission_classes_by_action = {
        'partial_update': [AdminProjectLevelPermissions],
        'update': [AdminProjectLevelPermissions]
    }

    def retrieve(self, request, pk=None, **kwars):
        queryset = Elements.objects.filter(category=pk)
        serializer = ElementsItemsSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        data = request.data
        queryset = Elements.objects.all()
        element = get_object_or_404(queryset, id=data['element']['id'])
        new_data = {'title': element.title, 'description': element.description, 'tags': element.tags,
                    'category': data['category_id'], 'order': element.order}
        element_serializer = ElementsSerializer(instance=element, data=new_data)
        if element_serializer.is_valid():
            element_serializer.save()
            return Response(element_serializer.data, 204)
        else:
            return Response(element_serializer.errors, 400)

class ReorderElementsVeiwSet(GenericModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes_by_action = {'update': [AdminProjectLevelPermissions]}

    def update(self, request, pk=None, *args, **kwargs):
        data = request.data
        print("DATA", data)
        queryset = Categories.objects.all()
        category = get_object_or_404(queryset, id=pk)
        new_data = {'name': category.name, 'description': category.description, 'section': category.section_id,
                    'order': data['order']}
        category_serializer = CategoriesSerializer(instance=category, data=new_data)
        if category_serializer.is_valid():
            category_serializer.save()
            return Response(category_serializer.data, 204)
        else:
            return Response(category_serializer.errors, 400)

class ReorderItemsVeiwSet(GenericModelViewSet):
    queryset = Elements.objects.all()
    serializer_class = ElementsSerializer
    permission_classes_by_action = {'update': [AdminProjectLevelPermissions]}

    def update(self, request, pk=None, *args, **kwargs):
        data = request.data
        print("DATA", data)
        queryset = Elements.objects.all()
        element = get_object_or_404(queryset, id=pk)
        new_data = {'title': element.title, 'description': element.description, 'category': element.category_id,
                    'order': data['order']}
        element_serializer = ElementsSerializer(instance=element, data=new_data)
        if element_serializer.is_valid():
            element_serializer.save()
            return Response(element_serializer.data, 204)
        else:
            return Response(element_serializer.errors, 400)

class ElementItemsViewSet(GenericModelViewSet):
    permission_classes_by_action = {
        'partial_update': [AdminProjectLevelPermissions],
        'update': [AdminProjectLevelPermissions]
    }

    def update(self, request, pk=None, *args, **kwargs):
        data = request.data
        queryset = Items.objects.all()
        item = get_object_or_404(queryset, id=pk)
        new_data = {'element': data['element_id'], 'type': item.type}
        item_serializer = ItemsSerializer(instance=item, data=new_data)
        if item_serializer.is_valid():
            item_serializer.save()
            return Response(item_serializer.data, 204)
        else:
            return Response(item_serializer.errors, 400)