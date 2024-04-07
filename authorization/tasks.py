from celery import shared_task
from time import sleep
from django.contrib.auth import get_user_model
import sys

# send sms to user
@shared_task(queue="queue_1")
def send_sms(phone_number,otp_code) :
    # sending email
    sys.stdout.write(otp_code)
    return phone_number

# delete user if not activate after 120s of registeration
@shared_task(queue="queue_1")
def delete_user(phone_number) :
    sleep(120)
    user = get_user_model().objects.get(phone=phone_number)
    if not user.is_active :
        user.delete()