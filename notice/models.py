# from django.db import models
#
# # Create your models here.
#
# class Filter(models.Model):
#     code = models.CharField(verbose_name='Код мобильного оператора', max_length=5, null=True)
#     tag = models.CharField(verbose_name='Тэг', max_length=100, null=True)
#
#     def __str__(self):
#         if self.code:
#             return self.code
#         else:
#             return  self.tag
#
#     class Meta:
#         verbose_name = 'Фильтр'
#         verbose_name_plural = 'Фильтры'
#
# class Notice(models.Model):
#     created = models.DateTimeField(verbose_name='Дата и время начала рассылки', auto_now_add=True)
#     text = models.TextField(verbose_name='Текст сообщения')
#
#     ended = models.DateTimeField(verbose_name='Дата и время окончания рассылки')
#     filters = models.ManyToManyField(Filter)
#     def __str__(self):
#         return str(self.created)
#
#     class Meta:
#         verbose_name = 'Рассылка'
#         verbose_name_plural = 'Рассылки'









from django.db import models

# Create your models here.

class Filter(models.Model):
    code = models.CharField(verbose_name='Код мобильного оператора', max_length=5, null=True)
    tag = models.CharField(verbose_name='Тэг', max_length=15, null=True)

    def __str__(self):
        if self.code:
            return self.code
        else:
            return  self.tag

    class Meta:
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтры'

class Notice(models.Model):
    created = models.DateField(verbose_name='Дата создания рассылки', auto_now_add=True)
    text = models.TextField(verbose_name='Текст сообщения')

    started = models.DateField(verbose_name='Дата отправки рассылки')
    ended = models.DateField(verbose_name='Дата окончания рассылки')

    def __str__(self):
        return str(self.created)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

class Notice_Filter(models.Model):
	notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name='filter_table')
	filter = models.ForeignKey(Filter, on_delete=models.SET_NULL, null = True, related_name='notice_table')

	@classmethod
	def create(cls,notice, filter):
		notice_filter = cls(notice=notice,filter=filter)
		return notice_filter




