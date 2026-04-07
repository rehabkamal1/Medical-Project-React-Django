# patients/views.py
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .models import Patient
from .serializers import (
    PatientSerializer, 
    PatientCreateUpdateSerializer,
    UserSerializer
)

User = get_user_model()

class PatientViewSet(viewsets.ModelViewSet):
    """ViewSet for Patient CRUD operations"""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action in ['create', 'update', 'partial_update']:
            return PatientCreateUpdateSerializer
        return PatientSerializer
    
    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['approve', 'block', 'unblock']:
            # Only allow admins for approval/blocking actions
            return [IsAdminUser()]
        elif self.action in ['update', 'partial_update']:
            # Allow update for authenticated users (admin or patients)
            return [permissions.IsAuthenticated()]
        elif self.action == 'destroy':
            # Only allow authenticated admins to delete
            return [IsAdminUser()]
        elif self.action in ['list', 'retrieve']:
            # Anyone can view
            return [permissions.AllowAny()]
        # Create for anyone
        return [permissions.AllowAny()]
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a patient"""
        patient = self.get_object()
        patient.is_approved = True
        patient.is_blocked = False
        patient.save()
        serializer = self.get_serializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        """Block a patient"""
        patient = self.get_object()
        patient.is_blocked = True
        patient.is_approved = False
        patient.save()
        serializer = self.get_serializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def unblock(self, request, pk=None):
        """Unblock a patient"""
        patient = self.get_object()
        patient.is_blocked = False
        patient.save()
        serializer = self.get_serializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PatientListView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.AllowAny]

class PatientCreateView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientCreateUpdateSerializer
    permission_classes = [permissions.AllowAny]

class PatientDetailView(generics.RetrieveUpdateAPIView):
    """Combined Retrieve and Update view"""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PatientCreateUpdateSerializer
        return PatientSerializer

    def get_object(self):
        if self.request.user.role == 'patient':
            return self.request.user.patient_profile
        return super().get_object()

class PatientUpdateView(generics.UpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        if self.request.user.role == 'patient':
            return self.request.user.patient_profile
        return super().get_object()

class PatientProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'patient':
            return Response(
                {"detail": "Only patients can access this endpoint."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        patient = request.user.patient_profile
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    def patch(self, request):
        if request.user.role != 'patient':
            return Response(
                {"detail": "Only patients can access this endpoint."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        patient = request.user.patient_profile
        serializer = PatientCreateUpdateSerializer(
            patient, 
            data=request.data, 
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientApprovalView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk, action):
        try:
            patient = Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=404)
        if action == 'approve':
            patient.is_approved = True
            patient.is_blocked = False
            patient.save()
            return Response({'status': 'approved'})
        elif action == 'block':
            patient.is_blocked = True
            patient.is_approved = False
            patient.save()
            return Response({'status': 'blocked'})
        elif action == 'unblock':
            patient.is_blocked = False
            patient.save()
            return Response({'status': 'unblocked'})
        else:
            return Response({'error': 'Invalid action'}, status=400)