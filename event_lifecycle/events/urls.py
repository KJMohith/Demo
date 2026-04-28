from django.urls import path

from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/add-user/', views.add_participant, name='add_participant'),
    path('dashboard/add-event/', views.add_event, name='add_event'),
    path('dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
    path('dashboard/participants/', views.participant_rows, name='participant_rows'),
    path('marks/<int:pk>/update/', views.update_marks, name='update_marks'),
    path('attendance/<int:pk>/toggle/', views.toggle_attendance, name='toggle_attendance'),
    path('feedback/<int:pk>/', views.feedback, name='feedback'),
    path('certificate/<uuid:hash>/', views.certificate, name='certificate'),
]
