# Django Imports
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Standard Package Imports
import os, json

# Project Imports
from .models import *
from prb import settings
from .tasks import contact_erp_task, get_last_fetched, set_last_fetched
from .helpers import alert_users, fetch_notices

# Third Party Imports
import requests


# Create your views here.

def register_tasks(request):
    contact_erp_task(repeat=600, repeat_until=None)
    # execute_from_command_line('process_tasks')
    return JsonResponse({
        'success': True,
        'message': 'Successfully registered all the tasks'
    })

def home(request):
    print(get_last_fetched())
    return JsonResponse({})