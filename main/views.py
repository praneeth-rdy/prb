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

# Third Party Imports
import requests


# Create your views here.

def home(request):
    return JsonResponse({
        'success': True,
        'message': 'You received this response'
    })

def fetch_erp(request):

    url = "https://erp.iitkgp.ac.in/TrainingPlacementSSO/ERPMonitoring.htm?action=fetchData&jqqueryid=54&_search=false&nd=1694657966755&rows=20&page=1&sidx=&sord=asc&totalrows=50"

    payload={}
    headers = {
    'Cookie': 'JSESSIONID=C9F6D0AEF8E62F986680A03495BF23C3.worker2; ssoToken=06C1958138B812592F43492696801D75.worker1D2B9E1A24773CF8A6C0CEACB7757545E.worker3DX0AI8Z0XDDLIY8W2SECM6JZX62QSTT8YCTC4Z8K38149AUGZCHCC8LI4OHPWGZ4; JSID#/IIT_ERP3=D2B9E1A24773CF8A6C0CEACB7757545E.worker3; JSID#/Academic=56BD13871E74F04AC89E8D081ECBBA4B.worker3; JSID#/TrainingPlacementSSO=C9F6D0AEF8E62F986680A03495BF23C3.worker2; JSESSIONID=B450616AC4928D7FC28C489A38538BE2.worker2',
    'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

    return JsonResponse({
        'success': True,
        'message': 'Fetched erp data'
    })