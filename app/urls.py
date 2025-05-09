from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('campaign/start/<int:campaign_id>/', views.start_campaign, name='start_campaign'),
]