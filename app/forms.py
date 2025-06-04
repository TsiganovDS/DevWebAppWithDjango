from django import forms

from app.models import Campaign, Message, Recipient


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ["full_name", "email", "comment"]



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]


class CampaignSendForm(forms.Form):
    campaign = forms.ModelChoiceField(
        queryset=Campaign.objects.all(), label="Выберите рассылку для отправки"
    )


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = [
            "subject",
            "body",
            "status",
            "created_at",
            "message",
            "start_time",
            "end_time",
        ]
