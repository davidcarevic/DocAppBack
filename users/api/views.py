from users.models import Users, EmailInvitation
from rest_framework_simplejwt.views import TokenObtainPairView
from users.api.serializers import UsersSerializer, MyTokenObtainPairSerializer, EmailInvitationSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from main.api.permissions import *
import uuid
from rest_framework.response import Response
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.shortcuts import get_object_or_404


class UsersViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes_by_action = {
        'create': [AllowAny],
        'list': [AdminPermission],
        'retrieve': [AdminPermission],
        'update': [IsOwnerOrReadOnly],
        'partial_update': [IsOwnerOrReadOnly],
        'destroy': [IsOwnerOrReadOnly]
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class EmailInvitationViewSet(ModelViewSet):
    queryset = EmailInvitation.objects.all()
    serializer_class = EmailInvitationSerializer
    permission_classes_by_action = {
        'retrieve': [AllowAny]
    }

    def retrieve(self, request, pk=None, **kwargs):
        queryset = EmailInvitation.objects.all()
        invite = get_object_or_404(queryset, token=pk)
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

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


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
