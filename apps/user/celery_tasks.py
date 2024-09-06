import random

from celery.app import shared_task
from django.core.cache import cache

from apps.user.rabbitmq import RabbitSmsOtp, RabbitEmailOtp


class OTPSender:
    def send(self, recipient, message):
        raise NotImplementedError("Subclasses must implement this method.")


class EmailSender(OTPSender):
    def send(self, recipient, message):
        rabbit_connection = RabbitEmailOtp()
        rabbit_connection.push({
            'to': recipient,
            'body': message
        })


class SMSSender(OTPSender):
    def send(self, recipient, message):
        rabbit_connection = RabbitSmsOtp()
        rabbit_connection.push({
            'to': recipient,
            'body': message
        })


def resolve_sender(recipient) -> OTPSender:
    if '@' in recipient:
        return EmailSender()
    return SMSSender()


@shared_task
def send_otp(recipient):
    code = random.randint(100000, 999999)
    cache.set(recipient, code, timeout=60 * 2)
    print(code)
    sender = resolve_sender(recipient)
    sender.send(recipient, code)
