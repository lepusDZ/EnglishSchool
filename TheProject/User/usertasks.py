from celery import shared_task
import requests
from .botCr import TELEGRAM_API_URL

@shared_task(ignore_result=True)
def send_message(data):
    return requests.post(TELEGRAM_API_URL + "sendMessage", data)