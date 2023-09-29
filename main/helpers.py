from django.core.mail import send_mail, EmailMessage

from prb import settings

import os, csv, re, requests, xmltodict

def alert_users(notices, recipients):
    if settings.DEBUG:
        recipients = ['k.praneeth1199@gmail.com']
    try:
        for notice in notices:
            email_options = {
                'subject': f"{notice['subject']} | {notice['type']} | {notice['company']}",
                'html_message': notice["body"] + f'<br/><br/> <b>Time</b>    : {notice["time"]}<br>',
                'from': settings.EMAIL_HOST_USER,
                'fail_silently': False,
            }
            email_response = send_mail(
                subject=email_options['subject'],
                message=email_options['html_message'],
                html_message=email_options['html_message'],
                from_email=email_options['from'],
                recipient_list=recipients,
                fail_silently=False,
            )
            print(email_response)
    except:
        print("Error while sending emails")


def fetch_notices(last_fetched):
    new_notices = []

    url = "https://erp.iitkgp.ac.in/TrainingPlacementSSO/ERPMonitoring.htm?action=fetchData&jqqueryid=54&_search=false&nd=1695958592456&rows=20&page=1&sidx=&sort=desc&totalrows=50"
    payload={}
    headers = {
    'Cookie': settings.COOKIE
    }
    response = requests.get(url, headers=headers, data=payload)


    # print(response)

    # print(response.text)

    try:
        all_notices = xmltodict.parse(response.text)["rows"]["row"]

        if last_fetched==None:
            return {
                "success": True,
                "message": "Your request is successfull",
                "data": [],
                "last_fetched": all_notices[0]["cell"][0],
            }

        for notice in all_notices:
            if int(notice["cell"][0]) > last_fetched:
                # notice_attachment = fetch_notice_attachment(notice_id=int(notice["cell"][0]))
                notice_body = fetch_notice_body(notice_id=int(notice["cell"][0]))
                formatted_notice = {
                    "type": notice["cell"][1],
                    "subject": notice["cell"][2],
                    "company": notice["cell"][3],
                    "body": notice_body,
                    "time": notice["cell"][6],
                    # "download": notice_attachment,
                }
                new_notices.append(formatted_notice)
                # print(notice)
            else:
                break
        
        # print(new_notices)
        return {
            "success": True,
            "message": "Your request is successfull",
            "data": new_notices,
            "last_fetched": all_notices[0]["cell"][0],
        }
    except:
        return {
            "success": False,
            "message": "Some unknown error"
        }
    # return {}


def fetch_notice_attachment(notice_id):

    url = f"https://erp.iitkgp.ac.in/TrainingPlacementSSO/AdmFilePDF.htm?type=NOTICE&year=2023-2024&id={notice_id}"

    payload={}
    headers = {
    'Cookie': settings.COOKIE
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.text:
        return response
    else:
        return None
    

def fetch_notice_body(notice_id):
    
    url = f"https://erp.iitkgp.ac.in/TrainingPlacementSSO/ShowContent.jsp?year=2023-2024&id={notice_id}"

    payload={}
    headers = {
    'Cookie': settings.COOKIE
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.text:
        pattern = r"<div[\s\S]*?</div>"
        match = re.search(pattern, response.text)
        print(match.group())
        return match.group()
    else:
        return None

def contact_erp():
    last_fetched = get_last_fetched()
    notices_response = fetch_notices(last_fetched=last_fetched)
    if not notices_response['success']:
        return {
            'success': False,
            'message': notices_response['message']
        }
    # print("Notices fetched", notices_response)
    alert_users(notices=notices_response["data"], recipients=settings.EMAIL_RECIPIENTS)
    if notices_response['success']:
        set_last_fetched(notices_response['last_fetched'])
    return {
        'success': True,
        'message': 'Contact successful'
    }

def get_last_fetched():
    with open(os.path.join(settings.BASE_DIR, 'main', 'var.csv'), 'r') as var_file:
        reader = csv.reader(var_file)
        first_row = next(reader)
    return int(first_row[1])

def set_last_fetched(set_val):
    with open(os.path.join(settings.BASE_DIR, 'main', 'var.csv'), 'w') as var_file:
        writer = csv.writer(var_file)
        writer.writerow(['last_fetched', set_val])