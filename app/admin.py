from django.contrib import admin
from .models import Recipient, Message, Campaign, SendingAttempt


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'comment',)
    list_filter = ('full_name',)
    search_fields = ('full_name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body')
    list_filter = ('subject',)
    search_fields = ('subject',)


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'status', 'message',)
    list_filter = ('start_time', 'status')
    search_fields = ('message__subject',)


@admin.register(SendingAttempt)
class SendingAttemptAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'attempt_time', 'status', 'server_response')
    list_filter = ('campaign',)
    search_fields = ('campaign__message__subject',)
