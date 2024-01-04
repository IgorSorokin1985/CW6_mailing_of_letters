from message.models import Message
from client.models import Client


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
