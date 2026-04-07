from rest_framework import serializers

from .models import (
    AdminDoctor,
    AdminPatient,
    AdminAppointment,
    AdminSpecialty,
    AdminSystemAlert,
    AdminNotification,
    AdminActivityLog
)

class AdminDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminDoctor
        fields = '__all__'

class AdminPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminPatient
        fields = '__all__'

class AdminAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminAppointment
        fields = '__all__'

class AdminSpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminSpecialty
        fields = '__all__'

class AdminSystemAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminSystemAlert
        fields = '__all__'

class AdminNotificationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%m/%d/%Y, %H:%M:%S")
    
    class Meta:
        model = AdminNotification
        fields = [
            'id', 'recipient_email', 'message', 'type', 
            'patient_name', 'doctor_name', 'appointment_date',
            'created_at', 'is_read'
        ]
        read_only_fields = ['created_at', 'id']

class AdminActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminActivityLog
        fields = '__all__'
