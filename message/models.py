from django.db import models
from client.models import Client
from notice.models import Notice

# Create your models here.
class Message(models.Model):
    created = models.DateField(verbose_name='Дата и время отправки', auto_now_add=True)
    status = models.CharField(verbose_name='Статус', max_length= 25)
    client = models.ForeignKey(Client, on_delete= models.SET_NULL, null = True, related_name='messages')
    notice = models.ForeignKey(Notice, on_delete= models.SET_NULL, null = True, related_name='messages')

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

