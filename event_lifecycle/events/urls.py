from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/add-user/', views.add_participant, name='add_participant'),
    path('dashboard/delete-user/<int:pk>/', views.delete_participant, name='delete_participant'),
    path('dashboard/add-event/', views.add_event, name='add_event'),
    path('dashboard/delete-event/<int:pk>/', views.delete_event, name='delete_event'),
    path('dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
    path('dashboard/participants/', views.participant_rows, name='participant_rows'),
    path('marks/<int:pk>/update/', views.update_marks, name='update_marks'),
    path('attendance/<int:pk>/toggle/', views.toggle_attendance, name='toggle_attendance'),
    path('feedback/<int:pk>/', views.feedback, name='feedback'),
    path('certificate/<uuid:hash>/', views.certificate, name='certificate'),
]
