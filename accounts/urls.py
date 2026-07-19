from django.urls import path
from .views import RegisterAPIView, ActivateAccountAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='auth-register'),
    path('activate/<uidb64>/<token>/', ActivateAccountAPIView.as_view(), name='auth-activate'),

]
