from background_task import background
from django.core.mail import EmailMessage


@background(schedule=60, remove_existing_tasks=True)
def contact_erp_task():
    print('Hello..')