from django.urls import path
from . import views

urlpatterns = [
    path('', views.complaint_list, name='complaint_list'),
    path('complaint/<int:pk>/', views.complaint_detail, name='complaint_detail'),
    path('complaint/<int:pk>/update-status/', views.complaint_update_status, name='complaint_update_status'),
    path('api/complaints/', views.complaint_api, name='complaint_api'),
]
