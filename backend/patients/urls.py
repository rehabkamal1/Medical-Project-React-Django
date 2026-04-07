# patients/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet,
    PatientProfileView,
    PatientApprovalView
)

router = DefaultRouter()
router.register(r'', PatientViewSet, basename='patient')

urlpatterns = [
    # Special routes first (to avoid conflicts with router)
    path('profile/', PatientProfileView.as_view(), name='patient-profile'),
    path('<int:pk>/<str:action>/', PatientApprovalView.as_view(), name='patient-approval'),
    # Then the router (which handles /, /<id>/, etc.)
    path('', include(router.urls)),
]