from django.db import models

# Create your models here.

class TimeZone(models.Model):
    code = models.CharField(verbose_name='Часовой пояс', max_length= 10)
    tag = models.CharField(verbose_name='Обозначение', max_length= 5)
    title = models.CharField(verbose_name='Наименование', max_length= 30)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Часовой пояс'
        verbose_name_plural = 'Часовой пояса'

class Client(models.Model):
    phone = models.CharField(verbose_name='Номер телефона', max_length=12, unique=True)
    code = models.CharField(verbose_name='Код мобильного оператора', max_length=5)
    tag = models.CharField(verbose_name='Тэг', max_length=15)

    time_zone = models.ForeignKey(TimeZone, on_delete= models.SET_NULL, null = True, related_name='clients')

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'