from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy


from app.models import Recipient, Campaign

from .forms import RecipientForm


class HomePageView(View):
    def get(self, request):
        total_campaigns = Campaign.objects.count()
        active_campaigns = Campaign.objects.filter(status='active').count()
        unique_recipients = Recipient.objects.count()
        context = {
            'total_campaigns': total_campaigns,
            'active_campaigns': active_campaigns,
            'unique_recipients': unique_recipients,
        }
        return render(request, 'app/home.html', context)


class RecipientListView(ListView):
    model = Recipient
    template_name = 'app/recipient_list.html'
    context_object_name = 'recipients'


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'app/recipient_create.html'
    success_url = reverse_lazy('app:recipient_list')

class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'app/recipient_update.html'
    success_url = reverse_lazy('app:recipient_list')

class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'app/recipient_confirm_delete.html'
    success_url = reverse_lazy('app:recipient_list')



