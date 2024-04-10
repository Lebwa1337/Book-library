import datetime
import os

import requests
from celery import shared_task

from borrowings.models import Borrowing

bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")


@shared_task
def send_tg_message(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.post(url)


@shared_task
def overdue_borrowings_notification():
    not_returned_borrowings = Borrowing.objects.filter(actual_return_date=None)
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    return_count = 0
    for borrowing in not_returned_borrowings:

        if borrowing.expected_return_date == tomorrow:
            send_tg_message(
                f"You have to return book: {borrowing.book}\n"
                f"Expected return date is: {borrowing.expected_return_date}"
            )
            return_count += 1

        if borrowing.expected_return_date < datetime.date.today():
            send_tg_message(
                f"Your borrowing is overdue."
                f"\nYou have to immediately return book: {borrowing.book}\n"
                f"Expected return date {borrowing.expected_return_date}"
            )
            return_count += 1

        if borrowing.expected_return_date == datetime.date.today():
            send_tg_message(
                f"Today is the last day to return book: {borrowing.book}\n"
                f"Expected return date {borrowing.expected_return_date}"
            )
            return_count += 1

    if return_count == 0:
        send_tg_message("No borrowings overdue today!")
