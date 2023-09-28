from background_task import background
from django.core.mail import send_mail, EmailMessage

import csv, os

from prb import settings

from .helpers import alert_users, fetch_notices


@background(schedule=60, remove_existing_tasks=True)
def contact_erp_task():
    last_fetched = get_last_fetched()
    notices_response = fetch_notices(last_fetched=last_fetched)
    print("Notices fetched", notices_response)
    alert_users(notices=notices_response["data"], recipients=settings.EMAIL_RECIPIENTS)
    if notices_response['success']:
        set_last_fetched(notices_response['last_fetched'])

def get_last_fetched():
    with open(os.path.join(settings.BASE_DIR, 'main', 'var.csv'), 'r') as var_file:
        reader = csv.reader(var_file)
        first_row = next(reader)
    return int(first_row[1])

def set_last_fetched(set_val):
    with open(os.path.join(settings.BASE_DIR, 'main', 'var.csv'), 'w') as var_file:
        writer = csv.writer(var_file)
        writer.writerow(['last_fetched', set_val])
