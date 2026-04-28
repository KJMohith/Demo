from django.contrib import admin

from .models import Event, Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'transaction_id', 'attendance', 'feedback_given')
    search_fields = ('name', 'email', 'transaction_id')
    list_filter = ('attendance', 'feedback_given')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'created_at')
    search_fields = ('title',)
