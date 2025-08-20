from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import RegistrationSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data['refresh']
        access = serializer.validated_data['access']

        data = {
            'detail' : "Login successful",
            'user': {
                'id' : serializer.validated_data['user'].id,
                'username': serializer.validated_data['user'].email
            }
        }


        response = Response({"message": "Tokens generated successfully"})

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
            refresh_token = request.COOKIES.get('refresh_token')
            
            if refresh_token is None:
                return Response({"detail" : "Refresh token not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = self.get_serializer(data={'refresh': refresh_token})
            
            try:
                serializer.is_valid(raise_exception=True)
            except:
                return Response({"detail": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
            
            access_token = serializer.validated_data.get("access")

            response = Response({"message": "access Token refreshed"})
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