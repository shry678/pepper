import json
from datetime import datetime

import requests
from flask import request, Response
from pytz import timezone

from models import Announcement
from pepper import settings
from pepper.app import DB, csrf

cst = timezone('US/Central')


def announcement_list():
    announcements = Announcement.query.all()
    announcement_list = []
    datetime_fmt = '%Y-%m-%d %H:%M:%S'
    for announcement in announcements:
        announcement_list.append({'text': announcement.text,
                                  'ts': datetime.strftime(announcement.timestamp, datetime_fmt)})
    return Response(json.dumps(announcement_list), mimetype='application/json')


@csrf.exempt
def create_announcement():
    token = request.form.get('token')
    text = request.form.get('text')
    ts = datetime.fromtimestamp(float(request.form.get('timestamp')))
    from_tz = timezone('UTC')
    ts = from_tz.localize(ts).astimezone(cst)
    if token != settings.SLACK_TOKEN:
        return 'Unauthorized', 401
    send_notification = text.startswith('<!channel>')
    if send_notification:
        text = text[text.find(' ') + 1:]
    announcement = Announcement(text, ts)
    DB.session.add(announcement)
    DB.session.commit()

    if send_notification:
        # Is this an Android notification?
        resp = requests.post('https://fcm.googleapis.com/fcm/send', headers={
            "Authorization": "key={}".format(settings.FIREBASE_KEY)
        }, json={
            "to": "/topics/announcements",
            "time_to_live": 0,
            "data": {
                "title": "HackTX",
                "text": text,
                "vibrate": "true"
            }
        })

        # Send iOS notification
        resp = requests.post('https://fcm.googleapis.com/fcm/send', headers={
            "Authorization": "key={}".format(settings.FIREBASE_KEY)
        }, json={
            "to": "/topics/ios",
            "priority": "high",
            "notification": {
                "title": "New Announcement!",
                "body": text
            }
        })

        # Send Slack announcement
        slack_data = {'text': text}

        resp = requests.post(
            settings.SLACK_WEBHOOK_URL, data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )
    # print resp.status_code

    # Create a POST to Firebase
    return 'Created announcement'
