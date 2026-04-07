from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .models import (
    AdminDoctor,
    AdminPatient,
    AdminAppointment,
    AdminSpecialty,
    AdminSystemAlert,
    AdminNotification,
    AdminActivityLog
)

from .serializers import (
    AdminDoctorSerializer,
    AdminPatientSerializer,
    AdminAppointmentSerializer,
    AdminSpecialtySerializer,
    AdminSystemAlertSerializer,
    AdminNotificationSerializer,
    AdminActivityLogSerializer
)

from .permissions import IsRoleAdmin

User = get_user_model()  

# Doctor ViewSet
class AdminDoctorViewSet(viewsets.ModelViewSet):
    queryset = AdminDoctor.objects.all()
    serializer_class = AdminDoctorSerializer
    permission_classes = [IsRoleAdmin]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        doctor = self.get_object()
        doctor.is_approved = True
        doctor.is_blocked = False
        doctor.save()
        return Response({'status': 'Doctor approved'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        doctor = self.get_object()
        doctor.is_blocked = True
        doctor.is_approved = False
        doctor.save()
        return Response({'status': 'Doctor blocked'}, status=status.HTTP_200_OK)

# Patient ViewSet
class AdminPatientViewSet(viewsets.ModelViewSet):
    queryset = AdminPatient.objects.all()
    serializer_class = AdminPatientSerializer
    permission_classes = [IsRoleAdmin]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        patient = self.get_object()
        patient.is_approved = True
        patient.is_blocked = False
        patient.save()
        return Response({'status': 'Patient approved'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        patient = self.get_object()
        patient.is_blocked = True
        patient.is_approved = False
        patient.save()
        return Response({'status': 'Patient blocked'}, status=status.HTTP_200_OK)

# Appointment ViewSet
class AdminAppointmentViewSet(viewsets.ModelViewSet):
    queryset = AdminAppointment.objects.all()
    serializer_class = AdminAppointmentSerializer
    permission_classes = [IsRoleAdmin]

# Specialty ViewSet
class AdminSpecialtyViewSet(viewsets.ModelViewSet):
    queryset = AdminSpecialty.objects.all()
    serializer_class = AdminSpecialtySerializer
    permission_classes = [IsRoleAdmin]

# System Alert ViewSet
class AdminSystemAlertViewSet(viewsets.ModelViewSet):
    queryset = AdminSystemAlert.objects.all()
    serializer_class = AdminSystemAlertSerializer
    permission_classes = [IsRoleAdmin]

# Notification ViewSet
class AdminNotificationViewSet(viewsets.ModelViewSet):
    queryset = AdminNotification.objects.all()
    serializer_class = AdminNotificationSerializer
    permission_classes = [IsRoleAdmin]

# Activity Log ViewSet
class AdminActivityLogViewSet(viewsets.ModelViewSet):
    queryset = AdminActivityLog.objects.all()
    serializer_class = AdminActivityLogSerializer
    permission_classes = [IsRoleAdmin]


# Admin Profile View
class AdminProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get admin profile information"""
        if not request.user.is_superuser:
            return Response(
                {"detail": "Only admins can access this endpoint."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user = request.user
        profile_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff,
            "date_joined": user.date_joined,
        }
        return Response(profile_data)

    def patch(self, request):
        """Update admin profile information"""
        if not request.user.is_superuser:
            return Response(
                {"detail": "Only admins can access this endpoint."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user = request.user
        
        # Update allowed fields
        if 'first_name' in request.data:
            user.first_name = request.data.get('first_name')
        if 'last_name' in request.data:
            user.last_name = request.data.get('last_name')
        if 'email' in request.data:
            user.email = request.data.get('email')
        
        # Only allow password change if current password is provided
        if 'password' in request.data and 'current_password' in request.data:
            if user.check_password(request.data.get('current_password')):
                user.set_password(request.data.get('password'))
            else:
                return Response(
                    {"detail": "Current password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        try:
            user.save()
            profile_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_superuser": user.is_superuser,
                "is_staff": user.is_staff,
                "date_joined": user.date_joined,
            }
            return Response(profile_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
