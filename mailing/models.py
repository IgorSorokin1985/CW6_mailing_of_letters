from django.db import models
from django.conf import settings
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
    name = models.CharField(max_length=50, verbose_name='Name mailing', **NULLABLE)
    data_mailing = models.DateTimeField(verbose_name='Datatime of mailing')
    periodicity = models.ForeignKey(Periodicity, on_delete=models.CASCADE, verbose_name='periodicity')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  **NULLABLE, verbose_name='Client id')
    status = models.CharField(max_length=50, verbose_name='Status mailing', **NULLABLE)

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        verbose_name = 'Mailing'
        verbose_name_plural = 'Mailings'
