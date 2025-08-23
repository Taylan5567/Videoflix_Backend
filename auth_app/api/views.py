from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import RegistrationSerializer, CustomTokenObtainPairSerializer, PasswordResetConfirmSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django_rq import get_queue
from .tasks import send_password_reset_email

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Register a new user as inactive and return a JWT access token.
        """
        serializer = RegistrationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        refresh_token = RefreshToken.for_user(user).access_token

        data = {
            "user": {
                "id": user.id,
                "email": user.email,
            },
            "token": str(refresh_token)
        }
        return Response(data, status=status.HTTP_201_CREATED)
        

class CookieTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        Authenticate user with email and password, set JWT tokens in HttpOnly cookies.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data['refresh']
        access = serializer.validated_data['access']

        user = serializer.user

        data = {
            'detail' : "Login successful",
            'user': {
                'id' : user.id,
                'username': user.username
            }
        }

        response = Response(data, status=status.HTTP_200_OK)

        response.set_cookie(
            key='access_token',
            value=access,
            httponly=True,
            secure=True,
            samesite='Lax'
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh,
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        return response
    
class CookieRefreshView(TokenRefreshView):        
        def post(self, request, *args, **kwargs):
            """
            Refresh the access token using refresh token from cookie.
            """
            refresh_token = request.COOKIES.get('refresh_token')
            
            if refresh_token is None:
                return Response({"detail" : "Refresh token not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = self.get_serializer(data={'refresh': refresh_token})
            
            try:
                serializer.is_valid(raise_exception=True)
            except:
                return Response({"detail": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
            
            access_token = serializer.validated_data.get("access")

            response = Response({"detail": "Token refreshed",
                                "access": access_token}, status=status.HTTP_200_OK)
            response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax'
            )

            return response          
        
class ActivateAccountView(APIView):
    authentication_classes = []
    permission_classes = []


    def get(self, request, uidb64: str, token: str):
        """
        Activate a user account given a UID and token from an email link.
        """
        try:
            user_pk = force_str(urlsafe_base64_decode(uidb64))
        except:
            return Response({"detail": "Invalid UID"}, status=status.HTTP_400_BAD_REQUEST)
        
        User = get_user_model()
        try:
            user_instance = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if not default_token_generator.check_token(user_instance, token):
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user_instance.is_active:
            return Response({"detail": "Account already activated"}, status=status.HTTP_200_OK)

        user_instance.is_active = True
        user_instance.save(update_fields=["is_active"])

        return Response({"detail": "Account activated successfully"}, status=status.HTTP_200_OK)
    

class LogoutView(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        """
        Log out user by blacklisting the refresh token and deleting cookies.
        """
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"detail": "No active session found"}, status=status.HTTP_400_BAD_REQUEST)
                
        response = Response({"detail": "Logout successful! All tokens will be deleted. Refresh token is now invalid."}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        RefreshToken(refresh_token).blacklist()
        response.cookie_options = {
            "path": "/",
            'httponly': True,
            'secure': True,
            'samesite': 'Lax'
        }
        
        return response
    

class PasswordresetView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        Enqueue a password reset email task if email corresponds to an active user.
        """
        email = request.data.get('email')
        if not email:
            return Response({"detail": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        User = get_user_model()
        try:
            user_instance = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if user_instance.is_active:
            queue_instance = get_queue("default")
            queue_instance.enqueue(send_password_reset_email, user_instance.id, job_timeout=900)
        return Response({"detail": "An email has been sent to reset your password."}, status=status.HTTP_200_OK)
    

class PasswordResetConfirmView(APIView):
    permission_classes = []
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64: str, token: str):
        """
        Confirm password reset given UID, token, and new password values.
        """
        try:
            user_pk = force_str(urlsafe_base64_decode(uidb64))
        except:
            return Response({"detail": "Invalid UID"}, status=status.HTTP_400_BAD_REQUEST)
        
        User = get_user_model()
        try:
            user_instance = User.objects.get(pk=user_pk) 
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if not default_token_generator.check_token(user_instance, token):
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get('new_password')
        if not new_password:
            return Response({"detail": "New password is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        confirm_password = request.data.get('confirm_password')
        if not confirm_password:
            return Response({"detail": "Confirm password is required"}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"detail": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        user_instance.set_password(new_password)
        user_instance.save(update_fields=["password"])

        return Response({"detail": "Your Password has been successfully reset."}, status=status.HTTP_200_OK)