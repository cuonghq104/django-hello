from django.contrib.auth.models import AnonymousUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import User
from api.serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer
from api.utils import CustomResponse
from api.constants import MessageCodes


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']

    def get_serializer_class(self):
        if self.action == 'register':
            return UserRegisterSerializer
        elif self.action == 'login':
            return UserLoginSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        print(serializer.data)
        return super().perform_create(serializer)

    def get_permissions(self):
        if self.action == 'register' or self.action == 'login':
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_authentication_classes(self):
        if self.action == 'login':
            # Skip JWT authentication for login to avoid token validation errors
            return [SessionAuthentication]
        return super().get_authentication_classes()

    @action(detail=False, methods=['post'], url_path='register', url_name='register')
    def register(self, request):
        serializer_data = self.get_serializer(data=request.data)
        if not serializer_data.is_valid():
            return CustomResponse.validation_error(
                MessageCodes.VALIDATION_ERROR, 
                serializer_data.errors
            )

        user = serializer_data.save()
        user_serializer = UserSerializer(user)
        return CustomResponse.created(
            user_serializer.data, 
            MessageCodes.USER_REGISTERED
        )

    @action(detail=False, methods=['post'], url_path='login', url_name='login')
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        print(email, password)
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                if not user.is_active:
                    return CustomResponse.unauthorized(MessageCodes.BLOCKED_USER)
                
                refresh = RefreshToken.for_user(user)
                return CustomResponse.success({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user': UserSerializer(user).data,
                }, MessageCodes.LOGIN_SUCCESS)
            else:
                return CustomResponse.unauthorized(MessageCodes.INVALID_CREDENTIALS)
        except User.DoesNotExist:
            return CustomResponse.unauthorized(MessageCodes.INVALID_CREDENTIALS)

    @action(detail=True, methods=['patch'], url_path='deactivate', url_name='deactivate')
    def deactivate(self, request, pk=None):
        try:
            user_data = User.objects.get(pk=pk)
            user_data.is_active = False
            user_data.save()
            return CustomResponse.success(
                UserSerializer(user_data).data, 
                MessageCodes.USER_DEACTIVATED
            )
        except User.DoesNotExist:
            return CustomResponse.not_found(MessageCodes.NOT_FOUND)
