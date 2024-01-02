from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True }
# Create your models here.


class Periodicity(models.Model):
    vars = models.CharField(max_length=50, verbose_name='Variants of periodicity')

    def __str__(self):
        return f'{self.vars}'

    class Meta:
        verbose_name = 'Variant'
        verbose_name_plural = 'Variants'


class Mailing(models.Model):
    data_mailing = models.DateTimeField(verbose_name='Datatime of mailing')
    periodicity = models.ForeignKey(Periodicity, on_delete=models.CASCADE, verbose_name='periodicity')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Client id')
    status = models.CharField(max_length=50, verbose_name='Status mailing', **NULLABLE)

    def __str__(self):
        return f'{self.data_mailing}'

    class Meta:
        verbose_name = 'Mailing'
        verbose_name_plural = 'Mailings'
