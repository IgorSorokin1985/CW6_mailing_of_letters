from django.db import models
from mailing.models import Mailing

NULLABLE = {'blank': True, 'null': True}
# Create your models here.


class Log(models.Model):
    datatime = models.DateTimeField(verbose_name='Datatime')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Mailing id')
    status = models.CharField(max_length=150, verbose_name='Status')
    answer_mail_server = models.CharField(max_length=150, verbose_name='Answer of mailserver')

    def __str__(self):
        return f'{self.datatime} {self.mailing}'

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
