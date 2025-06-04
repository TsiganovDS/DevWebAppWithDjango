from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.conf import settings


class Recipient(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="Фамилия Имя")
    email = models.EmailField(unique=True)
    comment = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Message(models.Model):
    subject = models.CharField(max_length=100)
    body = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
        default=1,
    )

    def __str__(self):
        return self.subject


class Campaign(models.Model):
    STATUS_CHOICES = [
        ("created", "Создана"),
        ("started", "Запущена"),
        ("completed", "Завершена"),
    ]

    subject = models.CharField(max_length=100, default="Без темы")
    body = models.TextField(default="")
    is_active = models.BooleanField(default=True, verbose_name='Создана')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    recipients = models.ManyToManyField(
        Recipient, verbose_name="Клиенты", related_name="campaigns", blank=True
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    start_time = models.DateTimeField(
        default=timezone.now, verbose_name="Дата и время первой отправки"
    )
    end_time = models.DateTimeField(
        default=timezone.now, verbose_name="Дата и время окончания отправки"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="campaigns",
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['owner']),
            models.Index(fields=['is_active']),
            models.Index(fields=['start_time']),
            models.Index(fields=['end_time']),
        ]

    def __str__(self):
        return f"Рассылка {self.pk} ({self.status})"

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Дата начала должна быть раньше даты окончания.")
        if not self.subject:
            raise ValidationError("Тема не может быть пустой.")
        if not self.body:
            raise ValidationError("Сообщение не может быть пустым.")

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.status == 'completed' or self.status == 'created':
            self.is_active = False
        else:
            self.is_active = True

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("app/campaign_list", kwargs={"pk": self.pk})

    @property
    def is_active_property(self):
        return self.status not in ['completed', 'created']



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



class SendingAttempt(models.Model):
    STATUS_CHOICES = [
        ("Успешно", "Успешно"),
        ("Не успешно", "Не успешно"),
    ]

    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    server_response = models.TextField()
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="attempts"
    )

    def __str__(self):
        return f"Попытка {self.campaign.pk} - {self.status}"
