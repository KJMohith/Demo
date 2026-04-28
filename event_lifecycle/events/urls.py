from django.urls import path

from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('attendance/<int:pk>/toggle/', views.toggle_attendance, name='toggle_attendance'),
    path('feedback/<int:pk>/', views.feedback, name='feedback'),
    path('certificate/<uuid:hash>/', views.certificate, name='certificate'),
]
