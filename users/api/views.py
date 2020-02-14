from users.models import Users, EmailInvitation
from rest_framework_simplejwt.views import TokenObtainPairView
from users.api.serializers import UsersSerializer, MyTokenObtainPairSerializer, EmailInvitationSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from main.api.permissions import *
from main.api.views import GenericModelViewSet
import uuid
from rest_framework.response import Response
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from main.api.serializers import TeamMembersSerializer,ProjectMembersSerializer

class UsersViewSet(GenericModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes_by_action = {
        'create': [AllowAny],
        'list': [IsAdminUser],
        'retrieve': [IsAdminOrOwner],
        'update': [IsAdminOrOwner],
        'partial_update': [IsAdminOrOwner],
        'destroy': [IsAdminOrOwner]
    }
    def create(self, request, *args, **kwargs):
        data = request.data
        serialized = UsersSerializer(data={'email': data['email'], 'password': data['password']})
        if serialized.is_valid():
            serialized.save()
            if data['data']['guid']:
                try:
                    serializer_team = TeamMembersSerializer(
                        data={'user': serialized.data["id"], 'team': data['data']['team'], 'role': 20})
                    if serializer_team.is_valid():
                        serializer_team.save()
                except:
                    pass
                try:
                    serializer_project = ProjectMembersSerializer(
                        data={'user': serialized.data["id"], 'project': data['data']['project'], 'role': 20})
                    if serializer_project.is_valid():
                        serializer_project.save()
                except:
                    pass
                invited = EmailInvitation.objects.filter(token=data['data']['guid']).get()
                invited.delete()
            return Response(serialized.data, status=201)
        else:
            return Response(serialized.errors, status=201)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class EmailInvitationViewSet(GenericModelViewSet):
    queryset = EmailInvitation.objects.all()
    serializer_class = EmailInvitationSerializer
    permission_classes_by_action = {
        'retrieve': [AllowAny]
    }

    def retrieve(self, request, pk=None, **kwargs):
        queryset = EmailInvitation.objects.all()
        invite = get_object_or_404(queryset, token=pk)
        if datetime.now().date() - invite.created_at.date() > timedelta(days=10):
            return Response(status=401)
        serializer = EmailInvitationSerializer(invite)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        data['token'] = str(uuid.uuid4())
        data['data']['user'] = request.user_meta['id']
        serialized = EmailInvitationSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            send_email(request)
            return Response(serialized.data, status=201)
        else:
            return Response(serialized.errors, status=201)

def send_email(request):
    print(request.data)
    message = Mail(
        from_email=request.user_meta['email'],
        to_emails=request.data['email']
    )
    try:
        if request.data['data']['type'] == 'team':
            message.dynamic_template_data = {
                'subject': 'Invitation to team',
                'text': 'You have been invited to join team %s.' % (request.data['data']['team']),
                'url': 'http://localhost:3000/register/' + request.data['token']
            }
        if request.data['data']['type'] == 'project':
            message.dynamic_template_data = {
                'subject': 'Invitation to project',
                'text': F'You have been invited to join a project %s.' % (request.data['data']['project_name']),
                'url': 'http://localhost:3000/register/' + request.data['token']
            }
    except:
        message.dynamic_template_data = {
            'subject': 'Invitation to project',
            'text': F'You have been invited to join Kroon',
            'url': 'http://localhost:3000/register/' + request.data['token']
        }

    message.template_id = 'd-6356bd9d31b740d08ea7c633d04f874d'
    try:
        sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
        response = sg.send(message)
    except Exception as e:
        print("ERROR: ", e)
