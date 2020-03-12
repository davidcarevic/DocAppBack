from users.models import Users, EmailInvitation, PasswordReset
from rest_framework_simplejwt.views import TokenObtainPairView
from users.api.serializers import UsersSerializer, MyTokenObtainPairSerializer, EmailInvitationSerializer, PasswordResetSerializer
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
        print('data je asdasdas ,', data)
        #checks if the user is a member of the app already, if so, just adds them to the proper project/team
        if data['data'].get('not_member') is False and data['data'].get('not_member') is not None:
            queryset = Users.objects.all()
            user = get_object_or_404(queryset, email=data['email'])
            if data['data']['guid'] is not None:
                try:
                    serializer_team = TeamMembersSerializer(
                        data={'user': user.id, 'team': data['data']['team'], 'role': 20})
                    if serializer_team.is_valid():
                        serializer_team.save()
                except:
                    pass
                try:
                    serializer_project = ProjectMembersSerializer(
                        data={'user': user.id, 'project': data['data']['project'], 'role': 20})
                    if serializer_project.is_valid():
                        serializer_project.save()
                except:
                    pass
                invited = EmailInvitation.objects.filter(token=data['data']['guid']).get()
                invited.delete()
            return Response(user.data, status=201)
        # creates a new user and adds them to a project/team if they're invited
        else:
            serialized = UsersSerializer(data={'email': data['email'], 'password': data['password']})
        if serialized.is_valid():
            serialized.save()
            if data['data'].get('guid') is not None:
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
        'retrieve': [AllowAny],
        'create': [AllowAny]
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
        EmailInvitation.objects.filter(email=data['email']).get()
        try:
            data['data']['not_member'] = False
        except:
            data['data']['not_member'] = True
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
    print(" u mejleru , data,", request.data)
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



class PasswordResetViewSet(GenericModelViewSet):
    queryset = PasswordReset.objects.all()
    serializer_class = PasswordResetSerializer
    permission_classes_by_action = {
        'retrieve': [AllowAny],
        'create': [AllowAny],
        'update': [AllowAny]
    }

    def retrieve(self, request, pk=None, **kwargs):
        queryset = PasswordReset.objects.all()
        reset = get_object_or_404(queryset, token=pk)
        if datetime.now().date() - reset.created_at.date() > timedelta(hours=2):
            return Response(status=401)
        serializer = PasswordResetSerializer(reset)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        print('request data: ', request)
        data['token'] = str(uuid.uuid4())
        serialized = PasswordResetSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            send_pass_reset_email(request)
            return Response(serialized.data, status=201)
        else:
            return Response(serialized.errors, status=201)

    def update(self, request, *args, **kwargs):
        data = request.data
        queryset = PasswordReset.objects.all();
        reset_req_user = get_object_or_404(queryset, token=data['guid'])
        new_data = {'email': reset_req_user.email, 'password': data['password']}
        user = Users.objects.filter(email=reset_req_user.email).get()
        user_serializer = UsersSerializer(instance=user, data=new_data)
        if user_serializer.is_valid():
            user_serializer.save()
            reset = PasswordReset.objects.filter(token=data['guid']).delete()
            if reset:
                return Response(user_serializer.data, 204)
            else:
                return Response(user_serializer.errors, 204)
        else:
            return Response(user_serializer.errors, 204)

def send_pass_reset_email(request):
    print(request.data)
    message = Mail(
        from_email="some_admin_mail@something.com",
        to_emails=request.data['email']
    )

    message.dynamic_template_data = {
        'subject': 'Knowledge Base | Password Reset',
        'text': F'You have requested to reset your password, please click the button and follow further instructions \n'
                F'If you have not requested this change, please ignore this email. \n \n',
        'url': 'http://localhost:3000/forgot-password/' + request.data['token']
    }

    message.template_id = 'd-6356bd9d31b740d08ea7c633d04f874d'
    try:
        sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
        response = sg.send(message)
    except Exception as e:
        print("ERROR: ", e)
