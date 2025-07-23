from django.urls import path
from . import views


urlpatterns = [
   path('main/', views.dashboard_view, name='dashboard'),
   path('api/complaint-data/', views.api_complaint_data, name='api_complaint_data'),
   path('complaint/<int:complaint_id>/', views.complaint_detail_view, name='complaint_detail'),
]
