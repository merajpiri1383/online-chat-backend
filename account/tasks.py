from celery import shared_task
from time import sleep
from django.contrib.auth import get_user_model
import sys
from django.shortcuts import get_object_or_404
from random import randint
from sms_ir import SmsIr
from django.conf import settings

# config sms service
sms_ir = SmsIr(
    api_key=settings.SMS_API_KEY,
    linenumber=settings.SMS_LINE_NUMBER
)

# send sms to user
@shared_task(queue="queue_1")
def send_sms(phone_number,otp_code) :
    # sending sms

    # sms_ir.send_sms(
    #     phone_number,
    #     f"کد ورود شما به کانکت {otp_code} می باشد ",
    #     settings.SMS_LINE_NUMBER,
    # )

    sys.stdout.write(otp_code)
    return phone_number

# delete user if not activate after 120s of registeration
@shared_task(queue="queue_2")
def delete_user(phone_number) :
    sleep(120)
    user = get_user_model().objects.get(phone=phone_number)
    if not user.is_active :
        user.delete()

@shared_task(queue="queue_1")
def forget_password(phone):
    user = get_object_or_404(get_user_model(),phone=phone)
    user.is_active = True
    # send sms
    sys.stdout.write(user.otp)
    # sending sms

    # sms_ir.send_sms(
    #     phone_number,
    #     f"کد ورود شما به کانکت {otp_code} می باشد ",
    #     settings.SMS_LINE_NUMBER,
    # )
    sleep(120)
    user.save()
    sys.stdout.write(user)