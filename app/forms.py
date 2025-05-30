from django import forms
from app.models import Recipient

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['full_name', 'email', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 1}),
        }