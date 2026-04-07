# patients/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Patient

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'date_joined']

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            'id', 'user', 'full_name', 'email', 'phone', 'address', 
            'age', 'date_of_birth', 'gender', 'blood_type', 'allergies', 
            'medical_history', 'is_approved', 'is_blocked',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_approved', 'is_blocked']

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_email(self, obj):
        return obj.user.email

class PatientCreateUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    last_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    email = serializers.EmailField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'email', 'password',
            'phone', 'address', 'age', 'gender', 'blood_type',
            'allergies', 'medical_history'
        ]
        extra_kwargs = {
            'phone': {'required': False, 'allow_blank': True},
            'address': {'required': False, 'allow_blank': True},
            'age': {'required': False, 'allow_null': True},
            'gender': {'required': False, 'allow_blank': True},
            'blood_type': {'required': False, 'allow_blank': True},
            'allergies': {'required': False, 'allow_blank': True},
            'medical_history': {'required': False, 'allow_blank': True},
        }

    def create(self, validated_data):
        # For CREATE, password is required
        if 'password' not in validated_data or not validated_data['password']:
            raise serializers.ValidationError({'password': 'Password is required when creating a patient.'})
            
        user_data = {
            'first_name': validated_data.pop('first_name', ''),
            'last_name': validated_data.pop('last_name', ''),
            'email': validated_data.pop('email', ''),
            'password': validated_data.pop('password'),
            'role': 'patient'
        }
        
        user = User.objects.create_user(**user_data)
        patient = Patient.objects.create(user=user, **validated_data)
        return patient

    def update(self, instance, validated_data):
        user = instance.user
        
        # Update user fields only if provided
        if 'first_name' in validated_data:
            user.first_name = validated_data.pop('first_name')
        if 'last_name' in validated_data:
            user.last_name = validated_data.pop('last_name')
        if 'email' in validated_data:
            user.email = validated_data.pop('email')
        if 'password' in validated_data and validated_data['password']:
            user.set_password(validated_data.pop('password'))
        else:
            # Remove password from validated_data if empty
            validated_data.pop('password', None)
            
        user.save()
        
        # Update patient fields only if provided
        for attr, value in validated_data.items():
            if value is not None:
                setattr(instance, attr, value)
            
        instance.save()
        return instance