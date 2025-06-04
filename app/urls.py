from django.urls import path

from . import views
from .views import (CampaignCreateView, CampaignDeleteView, CampaignDetailView,
                    CampaignListView, CampaignUpdateView, MessageCreateView,
                    MessageDeleteView, MessageDetailView, MessageListView,
                    MessageUpdateView, RecipientCreateView,
                    RecipientDeleteView, RecipientListView,
                    RecipientUpdateView, SendingAttemptListView)

app_name = "app"


urlpatterns = [
    path("", views.home_view, name="home"),
    path("recipient/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("recipients/", RecipientListView.as_view(), name="recipient_list"),
    path(
        "recipient/edit/<int:pk>/",
        RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipient/delete/<int:pk>/",
        RecipientDeleteView.as_view(),
        name="recipient_delete",
    ),
    path("messages/", MessageListView.as_view(), name="messages_list"),
    path("messages/add/", MessageCreateView.as_view(), name="message_create"),
    path("messages/<int:pk>/edit/", MessageUpdateView.as_view(), name="message_update"),
    path(
        "messages/<int:pk>/delete/",
        MessageDeleteView.as_view(),
        name="message_confirm_delete",
    ),
    path("messages/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("campaigns/", CampaignListView.as_view(), name="campaign_list"),
    path("campaigns/<int:pk>/", CampaignDetailView.as_view(), name="campaign_detail"),
    path(
        "campaign/<int:pk>/delete/",
        CampaignDeleteView.as_view(),
        name="campaign_confirm_delete",
    ),
    path("campaign_send/<int:pk>/", views.campaign_send, name="campaign_send"),
    path("campaign/create/<int:message_id>", CampaignCreateView.as_view(), name="campaign_create"),
    path("campaign/<int:pk>/edit/", CampaignUpdateView.as_view(), name="campaign_edit"),
    path(
        "campaigns/attempts/",
        SendingAttemptListView.as_view(),
        name="campaign_attempt_list",
    ),
]
