from rest_framework import permissions
from rest_framework_role_filters.role_filters import RoleFilter
from restfw_composed_permissions.base import (BaseComposedPermission, And, Or)
from restfw_composed_permissions.generic.components import (AllowAll, AllowOnlyAuthenticated, AllowOnlySafeHttpMethod)
from rest_condition import ConditionalPermission, C, And, Or, Not
from rest_framework_role_filters.viewsets import RoleFilterModelViewSet


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = 'You must be the owner to edit or delete this object.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id


class AdminPermission(permissions.BasePermission):
    message = 'You have to be admin to perform this action.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        for inst in request.user_meta['teams']:
            if inst['id'] == 1 and inst['role'] == 0:
                return True
        return False


class EditorPermission(permissions.BasePermission):
    message = 'You have to be editor to perform this action.'
    safe_methods = ('GET', 'POST', 'PUT', 'PATCH')

    def has_object_permission(self, request, view, obj):
        if request.method in self.safe_methods:
            return True
        for inst in request.user_meta['teams']:
            if obj.team.id == inst['id'] and inst['role'] == 10:
                return True
        return False


class ViewerPermission(permissions.BasePermission):
    message = 'You are restricted to viewer mode.'

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class Perm(permissions.BasePermission):
    message = "NO!"

    def has_object_permission(self, request, view, obj):
        try:
            return obj.element.category.section.project.id == 10
        except:
            try:
                print(obj.category.section.project.id)
                return obj.category.section.project.id == 1
            except:
                try:
                    print(obj.section.project.id)
                    return obj.section.project.id == 1
                except:
                    try:
                        print(obj.project.id)
                        return obj.project.id == 1
                    except:
                        return False
