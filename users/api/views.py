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

    def create(self, request, *args, **kwargs):
        data = request.data
        data['token'] = str(uuid.uuid4())
        serialized = EmailInvitationSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            send_email(request, request.data['email'])
            return Response(serialized.data, status=201)
        else:
            return Response(serialized._errors, status=201)



def send_email(request, email):
    message = Mail(
        from_email=request.user_meta['email'],
        to_emails=email
    )
    message.dynamic_template_data = {
        'subject': 'Invitation',
        'text': 'You have been invited to join Kroon studio team.',
        'url': 'google.rs'
    }
    message.template_id = 'd-6356bd9d31b740d08ea7c633d04f874d'
    try:
        sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(response.status_code, response.body, response.headers)
    except Exception as e:
        print("ERROR: ", e)