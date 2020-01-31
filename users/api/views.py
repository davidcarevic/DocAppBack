from users.models import Users
from users.api.serializers import UsersSerializer
from rest_framework.viewsets import ViewSet
from rest_framework import filters, status, generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class UsersViewSet(ViewSet):
    def list(self, request):
        queryset = Users.objects.all()
        serializer = UsersSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Users.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UsersSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        data=request.data
        serialized = UsersSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=201)
        else:
            return Response(serialized._errors, status=201)

    def update(self, request, pk=None):
        inst = Users.objects.get(pk=pk)
        data = request.data
        serialized = UsersSerializer(instance=inst, data=data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=201)
        else:
            return Response(serialized._errors, status=201)

    def partial_update(self, request, pk=None):
        inst = Users.objects.get(pk=pk)
        data = request.data
        serialized = UsersSerializer(instance=inst, data=data, partial=True)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=201)
        else:
            return Response(serialized._errors, status=201)

    def destroy(self, request, pk=None):
        users = Users.objects.get(pk=pk)
        users.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
