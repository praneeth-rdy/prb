from django.core.mail import send_mail, EmailMessage

from prb import settings

import requests, xmltodict

def alert_users(notices, recipients):
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

    url = "https://erp.iitkgp.ac.in/TrainingPlacementSSO/ERPMonitoring.htm?action=fetchData&jqqueryid=54&_search=false&nd=1694657966755&rows=20&page=1&sidx=&sort=desc&totalrows=50"
    payload={}
    headers = {
    'Cookie': settings.COOKIE
    }
    response = requests.request("GET", url, headers=headers, data=payload)


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
    'Cookie': 'JSESSIONID=9310CE01109F81E80E5C83921A4F12BE.worker2; ssoToken=F211415D3F2E8457F75E079849D67FA0.worker17C58F5782CFFEE7664C4CA3C848842B8.worker3MRCLSWXS2L40ENC466VWFTKP9VBBGLSA28OUSVSH7Y8YO95R7C4GHH4NDIE1B5O7; JSID#/IIT_ERP3=7C58F5782CFFEE7664C4CA3C848842B8.worker3; JSID#/Academic=1D6126DB18B65708103272A324716C61.worker3; JSID#/TrainingPlacementSSO=9310CE01109F81E80E5C83921A4F12BE.worker2; JSESSIONID=B450616AC4928D7FC28C489A38538BE2.worker2'
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
    'Cookie': 'JSESSIONID=9310CE01109F81E80E5C83921A4F12BE.worker2; ssoToken=F211415D3F2E8457F75E079849D67FA0.worker17C58F5782CFFEE7664C4CA3C848842B8.worker3MRCLSWXS2L40ENC466VWFTKP9VBBGLSA28OUSVSH7Y8YO95R7C4GHH4NDIE1B5O7; JSID#/IIT_ERP3=7C58F5782CFFEE7664C4CA3C848842B8.worker3; JSID#/Academic=1D6126DB18B65708103272A324716C61.worker3; JSID#/TrainingPlacementSSO=9310CE01109F81E80E5C83921A4F12BE.worker2; JSESSIONID=B450616AC4928D7FC28C489A38538BE2.worker2'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.text:
        return response.text
    else:
        return None

