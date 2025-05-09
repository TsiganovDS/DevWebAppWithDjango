from django.db import models

class Recipient(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200)
    comment = models.TextField(blank=True)


    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject


class Campaign(models.Model):
    STATUS_CHOICES = [
        ('Создана', 'Создана'),
        ('Запущена', 'Запущена'),
        ('Завершена', 'Завершена'),
    ]
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Создана')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient)

    def __str__(self):  # Fixed method name
        return f"Рассылка {self.id} - {self.status}"


class SendingAttempt(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='attempts')
    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=[('Успешно', 'Успешно'), ('Не успешно', 'Не успешно')])
    server_response = models.TextField()

    def __str__(self):  # Fixed method name
        return f"Попытка {self.id} - {self.status}"
