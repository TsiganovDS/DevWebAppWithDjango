from django.urls import path

from .views import RecipientCreateView, RecipientUpdateView, RecipientListView, RecipientDeleteView, HomePageView

app_name = 'app'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('recipient/create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipients/', RecipientListView.as_view(), name='recipient_list'),
    path('recipient/edit/<int:pk>/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient/delete/<int:pk>/', RecipientDeleteView.as_view(), name='recipient_delete'),
]