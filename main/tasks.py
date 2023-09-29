from background_task import background
from django.core.mail import send_mail, EmailMessage

from prb import settings

from .helpers import contact_erp


@background(schedule=60, remove_existing_tasks=True)
def contact_erp_task():
    contact_erp()

