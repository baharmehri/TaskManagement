import random

from celery.app import shared_task
from django.core.cache import cache


# @shared_task
def send_otp(recipient):
    code = random.randint(100000, 999999)
    cache.set(recipient, code, timeout=60 * 2)
    print(code)
