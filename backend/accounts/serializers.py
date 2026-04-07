# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# accounts/serializers.py

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'role', 'specialization']
        extra_kwargs = {'password': {'write_only': True}, 'specialization': {'required': False, 'allow_blank': True}}

    def create(self, validated_data):
        specialization = validated_data.pop('specialization', None)
        user = CustomUser.objects.create_user(**validated_data)
        if user.role == 'doctor' and specialization:
            user.specialization = specialization
            user.save()
        return user

    def to_representation(self, instance):
        data = {
            "id": instance.id,
            "username": instance.username,
            "email": instance.email,
            "role": instance.role
        }
        if instance.role == 'doctor':
            data["specialization"] = getattr(instance, 'specialization', '')
        return data

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # If user is superuser, set role to 'admin'
        user_role = 'admin' if user.is_superuser else user.role
        token['role'] = user_role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # If user is superuser, set role to 'admin'
        user_role = 'admin' if self.user.is_superuser else self.user.role
        data['role'] = user_role
        return data

class EmailTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'email': ['No user with this email.']})
        if not user.check_password(password):
            raise serializers.ValidationError({'password': ['Incorrect password.']})
        if not user.is_active:
            raise serializers.ValidationError({'email': ['User account is disabled.']})
        refresh = RefreshToken.for_user(user)
        
        # If user is superuser, set role to 'admin'
        user_role = 'admin' if user.is_superuser else user.role
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': user_role,
            'username': user.username,
        }

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'specialization']
        read_only_fields = ['id', 'role']
        extra_kwargs = {
            'specialization': {'required': False, 'allow_blank': True}
        }
    
    def get_role(self, obj):
        # If user is superuser, return 'admin'
        if obj.is_superuser:
            return 'admin'
        return obj.role