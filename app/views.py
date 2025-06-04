from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from app.models import Campaign, Message, Recipient, SendingAttempt

from .forms import RecipientForm


@cache_page(60 * 2)
def home_view(request):
    total_campaigns = Campaign.objects.count()
    active_campaigns = Campaign.objects.filter(status="active").count()
    unique_recipients = Recipient.objects.count()
    context = {
        "total_campaigns": total_campaigns,
        "active_campaigns": active_campaigns,
        "unique_recipients": unique_recipients,
    }
    return render(request, "app/home.html", context)


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "app/recipient_list.html"
    context_object_name = "recipients"


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "app/recipient_create.html"
    success_url = reverse_lazy("app:recipient_list")


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "app/recipient_update.html"
    success_url = reverse_lazy("app:recipient_list")


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = "app/recipient_confirm_delete.html"
    success_url = reverse_lazy("app:recipient_list")


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "app/messages_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Message.objects.all()
        return Message.objects.filter(owner=user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "app/message_detail.html"
    context_object_name = "message"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Message.objects.all()
        return Message.objects.filter(owner=user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "app/message_create.html"
    success_url = reverse_lazy("app:messages_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "app/message_update.html"
    success_url = reverse_lazy("app:messages_list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "app/message_confirm_delete.html"
    success_url = reverse_lazy("app:messages_list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


def campaign_send(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)

    if campaign.owner != request.user:
        messages.error(request, "У вас нет прав на отправку этой рассылки.")
        return redirect("app:campaign_detail", pk=pk)

    recipients = campaign.recipients.all()
    success_count = 0

    for recipient in recipients:
        try:
            send_mail(
                subject=campaign.message.subject,
                message=campaign.message.body,
                from_email=None,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            status = "Успешно"
            response = "OK"
            success_count += 1
        except Exception as e:
            status = "Не успешно"
            response = str(e)

        SendingAttempt.objects.create(
            campaign=campaign,
            status=status,
            server_response=response,
        )

    campaign.status = "Запущена"
    campaign.save()

    messages.success(
        request,
        f"Рассылка отправлена. Успешно: {success_count}/{recipients.count()}",
    )
    return redirect("app:campaign_detail", pk=pk)


class CampaignDetailView(LoginRequiredMixin, DetailView):
    model = Campaign
    template_name = "app/campaign_detail.html"
    context_object_name = "campaign"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Campaign.objects.all()
        return Campaign.objects.filter(owner=user)


class CampaignListView(LoginRequiredMixin, ListView):
    model = Campaign
    template_name = "app/campaign_list.html"
    context_object_name = "campaigns"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = Message.objects.first()
        context['active_campaigns_count'] = Campaign.objects.filter(status='started').count()
        context['active_campaigns_list'] = Campaign.objects.filter(status='started')
        return context

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Campaign.objects.all()
        return Campaign.objects.filter(owner=user)

    def main_page(request):
        campaigns = Campaign.objects.filter(is_active=True)
        total_campaigns = Campaign.objects.count()
        active_campaigns = campaigns.count()

        context = {
            'campaigns': campaigns,
            'total_campaigns': total_campaigns,
            'active_campaigns': active_campaigns,
        }
        return render(request, 'app/home.html', context)



class CampaignDeleteView(LoginRequiredMixin, DeleteView):
    model = Campaign
    template_name = "app/campaign_confirm_delete.html"
    success_url = reverse_lazy("app:campaign_list")

    def get_queryset(self):
        return Campaign.objects.filter(owner=self.request.user)


class CampaignCreateView(LoginRequiredMixin, CreateView):
    model = Campaign
    template_name = "app/campaign_create.html"
    fields = ["start_time", "end_time", "status", "message", "recipients"]
    success_url = reverse_lazy("app:campaign_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = Message.objects.get(pk=self.kwargs['message_id'])
        return context


class CampaignUpdateView(LoginRequiredMixin, UpdateView):
    model = Campaign
    fields = ["start_time", "end_time", "status", "message", "recipients"]
    template_name = "app/campaign_edit.html"
    success_url = reverse_lazy("app:campaign_list")

    def get_queryset(self):
        return Campaign.objects.filter(owner=self.request.user)


class SendingAttemptListView(LoginRequiredMixin, ListView):
    model = SendingAttempt
    template_name = "app/campaign_attempt_list.html"
    context_object_name = "attempts"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return SendingAttempt.objects.all()
        return SendingAttempt.objects.filter(campaign__owner=user)
