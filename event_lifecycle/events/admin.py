from django.contrib import admin

from .models import Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'transaction_id', 'transaction_verified', 'attendance', 'feedback_given')
    search_fields = ('name', 'email', 'transaction_id')
    list_filter = ('transaction_verified', 'attendance', 'feedback_given')
