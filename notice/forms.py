
from .models import Filter

import datetime


def is_valid(started, ended, text, filters):
    if filters is None:
        filters = []
    context = {'error': False}
    messages = []
    if started == '' or started == None:
        messages.append("Не была выбрана дата начала рассылки")
        context['error'] = True
    if ended == '' or ended == None:
        messages.append("Не была выбрана дата окончания")
        context['error'] = True
    else:
        try:
            ended = datetime.datetime.strptime(ended, "%Y-%m-%d").date()
            started = datetime.datetime.strptime(started, "%Y-%m-%d").date()
        except:
            messages.append("Формат данных начала и конца рассылки не подлежит конвертации в date")
            context['error'] = True
            ended = datetime.date.today()
            started = datetime.date.today()
        if (ended <= datetime.date.today()):
            messages.append("Дата окончания рассылки должен быть позже сегоднешнего числа")
            context['error'] = True
        if (ended <= started):
            messages.append("Дата окончания рассылки должен быть позже даты начала рассылки")
            context['error'] = True
    if (len(text) < 20):
        messages.append(
            "Количество символов в тексте письма должно быть больше 20 на данный момент: " + str(len(self.text)))
        context['error'] = True
    if (len(filters) == 0):
        messages.append("Должны быть выбраны фильтры для рассылки")
        context['error'] = True
    else:
        for filter in filters:
            if Filter.objects.filter(id=filter).get():
                pass
            else:
                messages.append("Выбранный фильтр не был найден, обновите страницу и создайте снова")
                context['error'] = True
                break

    context['messages'] = messages

    return context