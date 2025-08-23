from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

class RegistrationSerializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirmed_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'email': {
                'required': True
            }
        }

    def validate_repeated_password(self, value):
        """
        Validate that password and confirmed_password match and 
        that the password meets Django's password validation criteria.
        """
        password = self.initial_data.get('password')
        if password and value and password != value:
            raise serializers.ValidationError('Passwords do not match')
        return value

    def validate_email(self, value):
        """
        Ensure the email address is unique in the user model.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def create(self, validated_data):
        """
        Create a new inactive user with the provided email and password.
        Username is set as the email.
        """
        User = get_user_model()
        email = validated_data["email"]
        password = validated_data["password"]
        user = User.objects.create_user(
            username=email,         
            email=email,            
            password=password,
            is_active=False
        )
        return user
    
User = get_user_model()
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def __init__(self, *args, **kwargs):
        """
        Remove the default username field since authentication is via email.
        """
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields.pop('username')

    def validate(self, attrs):
        """
        Validate user credentials with email and password.
        Populate 'username' in attrs for JWT processing.
        """
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password')
        
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid email or password')

        attrs['username'] = user.username
        data = super().validate(attrs)
        return data

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        """
        Validate that the new_password and confirm_password are identical 
        and that new_password meets Django's password validation requirements.
        """
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs