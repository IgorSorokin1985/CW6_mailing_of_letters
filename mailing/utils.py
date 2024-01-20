import datetime
import pytz
from message.models import Message
from client.models import Client
from mailing.models import Mailing
from log.models import Log
from datetime import timedelta
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


def check_status_mailing(mailing):
    """
    This function for checking mailing' status. If all is ok - change Status on Ready.
    """
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
    """
    This function for execution of mailing.
    """
    if check_date_mailing_finish(mailing):
        mailing = Mailing.objects.get(pk=mailing.pk)
        message = Message.objects.get(mailing=mailing.pk)
        clients = Client.objects.filter(mailing=mailing.pk).all()
        answers = []
        success_attempt = 0
        unsuccessful_attempt = 0
        for client in clients:
            try:
                print('email host')
                print(EMAIL_HOST_USER)
                print('end email host')
                answer = send_mail(
                    subject=message.title,
                    message=get_letter(client, message),
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[client.email]
                )
                answers.append(f'Mailing - {mailing.name}, Date - {datetime.datetime.now()}, {client.email} - {answer}/n')
                success_attempt += 1
            except Exception:
                print('Error')
                answers.append(f'Mailing - {mailing.name}, Date - {datetime.datetime.now()}, {client.email} - Error/n')
                unsuccessful_attempt += 1
        add_history_of_mailing(mailing, answers, success_attempt, unsuccessful_attempt)
        if success_attempt > 0:
            add_new_datetime(mailing)
    else:
        mailing.status = 'Finished'
        mailing.save()


def add_new_datetime(mailing):
    """
    If the mailing is repeated, then this function sets a new time.
    """
    if mailing.periodicity_id == 1:
        mailing.status = 'Finished'
    elif mailing.periodicity_id == 2:
        mailing.data_mailing = datetime.datetime.now() + timedelta(days=1)
    elif mailing.periodicity_id == 3:
        mailing.data_mailing = datetime.datetime.now() + timedelta(days=7)
    if check_date_mailing_finish(mailing):
        mailing.status = 'Finished'
    mailing.save()


def add_history_of_mailing(mailing, answers, success_attempt, unsuccessful_attempt):
    """
    This function for adding history about sending in mailing's log.
    """
    new_log = {
        "datatime": datetime.datetime.now(),
        "mailing": mailing,
        "status": f"Success - {success_attempt}, Unsuccessful - {unsuccessful_attempt}",
        "answer_mail_server": answers,
    }
    Log.objects.create(**new_log)


def send_ready_mailings():
    """
    This function is finding mailing with status Ready and expired date. And start sending message to clients
    (if such mailings were found).
    """
    utc = pytz.UTC
    now = datetime.datetime.now().replace(tzinfo=utc)
    mailings = Mailing.objects.filter(status='Ready').all()
    count = 0
    for mailing in mailings:
        datetime_mailing = mailing.data_mailing.replace(tzinfo=utc)
        if now > datetime_mailing:
            if check_date_mailing_finish(mailing):
                mailing_execution(mailing.pk)
                count += 1
            else:
                mailing.status = 'Finished'
                mailing.save()
    if count > 0:
        print(f'All mailings with the Ready status have been completed. Total {count} mailings.')
    else:
        print('I did not find mailings with the Ready status. I will try in the near future...')


def sorting_list_mailings(mailings_list):
    """
    Function for sorting mailings.
    return: contex with  mailing_list and finished_list
    """
    finished_list = []
    result_list = []
    if len(mailings_list) > 0:
        for mailing in mailings_list:
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


def get_letter(client, message):
    """
    Function for creating letter for client.
    """
    result = f'Hello {client.name} {client.lastname},/n{message.body}'
    return result


def check_date_mailing_finish(mailing):
    if mailing.data_mailing_finish:
        utc = pytz.UTC
        now = datetime.datetime.now().replace(tzinfo=utc)
        if mailing.data_mailing_finish > now:
            return True
        else:
            return False
    else:
        return True
