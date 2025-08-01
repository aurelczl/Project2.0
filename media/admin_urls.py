from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_public_library, name='admin_public_library'),
]
