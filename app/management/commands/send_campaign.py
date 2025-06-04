from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from app.models import Campaign, SendingAttempt


class Command(BaseCommand):
    help = "Отправляет все активные рассылки"

    def handle(self, *args, **options):
        now = timezone.now()
        campaigns = Campaign.objects.filter(
            status="Создана", start_time__lte=now, end_time__gte=now
        )

        for campaign in campaigns:
            self.stdout.write(f"📨 Отправляем рассылку #{campaign.pk}")
            success_count = 0

            for recipient in campaign.recipients.all():
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
                    campaign=campaign, status=status, server_response=response
                )

            campaign.status = "Запущена"
            campaign.save()

            self.stdout.write(
                f"✅ Рассылка #{campaign.pk} отправлена ({success_count}/{campaign.recipients.count()})"
            )
