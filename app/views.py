from django.utils import timezone

from django.shortcuts import render, redirect, get_object_or_404
from .models import Campaign, Recipient

def start_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    if campaign.status != 'Запущена':
        campaign.status = 'Запущена'
        campaign.start_time = timezone.now()
        campaign.save()
        # Тут можно запустить асинхронную задачу рассылки
    return redirect('home')

def home(request):
    total_campaigns = Campaign.objects.count()
    active_campaigns = Campaign.objects.filter(status='Запущена').count()
    unique_recipients = Recipient.objects.count()
    context = {
        'total_campaigns': total_campaigns,
        'active_campaigns': active_campaigns,
        'unique_recipients': unique_recipients,
    }
    return render(request, 'home.html', context)
