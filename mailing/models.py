from django.db import models
from message.models import Message
from client.models import Client

NULLABLE = {'blank': True, 'null': True }
# Create your models here.

class Mailing(models.Model):
    data_mailing = models.DateTimeField(verbose_name='Datatime of mailing')
    is_periodicity = models.BooleanField(verbose_name='Periodicity')
    #period = models.IntegerChoices
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Message id')
    clients = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Client id')

    def __str__(self):
        return f'{self.data_mailing}'

    class Meta:
        verbose_name = 'Mailing'
        verbose_name_plural = 'Mailings'
