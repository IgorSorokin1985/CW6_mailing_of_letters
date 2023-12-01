from django.db import models

NULLABLE = {'blank': True, 'null': True }


# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    lastname = models.CharField(max_length=50, verbose_name='Lastname')
    birthday = models.DateField(verbose_name='Birthday', **NULLABLE)
    email = models.EmailField(max_length=50, verbose_name='Email')
    comment = models.CharField(max_length=300, verbose_name='Comment', **NULLABLE)

    def __str__(self):
        return f'{self.name} {self.lastname}'

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
