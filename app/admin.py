from django.contrib import admin

from .models import Campaign, Message, Recipient, SendingAttempt


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'country', 'avatar')
    list_filter = ("full_name",)
    search_fields = ("full_name",)


0


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "body")
    list_filter = ("subject",)
    search_fields = ("subject",)


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("pk", "owner", "status", "start_time", "get_recipients_count")
    list_filter = ("status", "owner", "start_time")

    @admin.display(description="Получателей")
    def get_recipients_count(self, obj):
        return obj.recipients.count()


@admin.register(SendingAttempt)
class SendingAttemptAdmin(admin.ModelAdmin):
    list_display = ("campaign", "status", "server_response")
    list_filter = (
        "status",
        "campaign",
    )
    search_fields = ("campaign__message__subject",)
