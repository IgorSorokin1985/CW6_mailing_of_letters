from django.db import models

NULLABLE = {'blank': True, 'null': True }
# Create your models here.


class Message(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title')
    body = models.TextField(verbose_name='Body of message')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
