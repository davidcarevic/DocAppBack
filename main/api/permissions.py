from rest_framework import permissions
from rest_framework_role_filters.role_filters import RoleFilter
from restfw_composed_permissions.base import (BaseComposedPermission, And, Or)
from restfw_composed_permissions.generic.components import (AllowAll, AllowOnlyAuthenticated, AllowOnlySafeHttpMethod)
from rest_condition import ConditionalPermission, C, And, Or, Not
from rest_framework_role_filters.viewsets import RoleFilterModelViewSet
from main.models import Roles

class IsOwnerOrReadOnly(permissions.BasePermission):
    message = 'You must be the owner to edit or delete this object.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id

class BaseTeamLevelPermissions(permissions.BasePermission):
    role = None
    message = ''

    def has_object_permission(self, request, view, obj):
        try:
            pass
        except KeyError:
            pass

        return False

class AdminProjectLevelPermissions(BaseTeamLevelPermissions):
    message = "You need to be admin to perform this action!"
    role = Roles.objects.get(name='admin')

class EditorProjectLevelPermission(BaseTeamLevelPermissions):
    message = "You need to have editor privileges to perform this action!"
    role = Roles.objects.get(name='editor')

class ViewerProjectLevelPermission(BaseTeamLevelPermissions):
    message = "You are restricted to viewer mode!"
    role = Roles.objects.get(name='viewer')

class BaseProjectLevelPermission(permissions.BasePermission):
    role = None
    message = ''

    def has_object_permission(self, request, view, obj):
        model_name = type(obj).__name__

        try:
            if model_name == "Items":
                return request.user_meta['project_access'][str(obj.element.category.section.project.id)] == self.role.id
            elif model_name == "Element":
                return request.user_meta['project_access'][str(obj.category.section.project.id)] == self.role.id
            elif model_name == "Category":
                return request.user_meta['project_access'][str(obj.section.project.id)] == self.role.id
            elif model_name == "Sections":
                return request.user_meta['project_access'][str(obj.project.id)] == self.role.id
            elif model_name == "Projects":
                return request.user_meta['project_access'][str(obj.id)] == self.role.id
        except KeyError:
            pass

        return False

class AdminProjectLevelPermissions(BaseProjectLevelPermission):
    message = "You need to be admin to perform this action!"
    role = Roles.objects.get(name='admin')

class EditorProjectLevelPermission(BaseProjectLevelPermission):
    message = "You need to have editor privileges to perform this action!"
    role = Roles.objects.get(name='editor')

class ViewerProjectLevelPermission(BaseProjectLevelPermission):
    message = "You are restricted to viewer mode!"
    role = Roles.objects.get(name='viewer')
