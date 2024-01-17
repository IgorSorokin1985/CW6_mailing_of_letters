import datetime
import pytz

from message.models import Message
from client.models import Client
from mailing.models import Mailing
from log.models import Log
from datetime import timedelta


def check_status_mailing(mailing):
    if mailing.status != 'Finished':
        if len(Message.objects.filter(mailing=mailing.pk).all()) > 0:
            if len(Client.objects.filter(mailing=mailing.pk).all()) > 0:
                return 'Ready'
            else:
                return 'Not ready'
        else:
            return 'Not ready'
    else:
        return 'Finished'


def mailing_execution(mailing):
    mailing = Mailing.objects.get(pk=mailing.pk)
    message = Message.objects.get(mailing=mailing.pk)
    clients = Client.objects.filter(mailing=mailing.pk).all()
    for client in clients:
        print(client.name)
        print(client.email)
        print(message.title)
        print(message.body)
    add_history_of_mailing(mailing)
    add_new_datetime(mailing)


def add_new_datetime(mailing):
    if mailing.periodicity_id == 1:
        mailing.status = 'Finished'
    elif mailing.periodicity_id == 2:
        mailing.data_mailing = datetime.datetime.now() + timedelta(days=1)
    elif mailing.periodicity_id == 3:
        mailing.data_mailing = datetime.datetime.now() + timedelta(days=7)
    mailing.save()


def add_history_of_mailing(mailing):
    new_log = {
        "datatime": datetime.datetime.now(),
        "mailing": mailing,
        "status": "Success",
        "answer_mail_server": 200,
    }
    Log.objects.create(**new_log)


def send_ready_mailings():
    utc = pytz.UTC

    now = datetime.datetime.now().replace(tzinfo=utc)

    mailings = Mailing.objects.filter(status='Ready').all()
    count = 0
    for mailing in mailings:
        datetime_mailing = mailing.data_mailing.replace(tzinfo=utc)
        if now > datetime_mailing:
            mailing_execution(mailing.pk)
            count += 1
    if count > 0:
        print(f'All mailings with the Ready status have been completed. Total {count} mailings.')
    else:
        print('I did not find mailings with the Ready status. I will try in the near future...')


def sorting_list_mailings(mailings_list):
    finished_list = []
    result_list = []
    if len(mailings_list) > 0:
        for mailing in mailings_list:
            print(mailing)
            result = {
                "mailing": mailing,
                "message": Message.objects.filter(mailing=mailing).last(),
                "number_of_clients": len(Client.objects.filter(mailing=mailing).all()),
                "number_of_times": len(Log.objects.filter(mailing=mailing).all()),
                "last_time": Log.objects.filter(mailing=mailing).last(),
            }
            if mailing.status == 'Ready':
                result['ready'] = True
            if mailing.status in ['Finished', 'Canceled']:
                finished_list.append(result)
            else:
                result_list.append(result)
    context = {
        "mailing_list": result_list,
        "finished_list": finished_list,
    }
    if len(finished_list) > 0:
        context["number_finished_mailings"] = len(finished_list)
    else:
        context["number_finished_mailings"] = False
    return context
