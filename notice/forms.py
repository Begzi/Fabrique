
from .models import Filter

import datetime




class NoticeValid:
    def __init__(self, started, ended, text, filters):

        self.started = started
        self.ended = ended
        self.text = text
        if filters is None:
            filters = []
        self.filters = filters
    def is_valid(self):
        context = {'error' : False }
        messages = []
        if self.started == '' or self.started == None:
            messages.append("Не была выбрана дата начала рассылки")
            context['error'] = True
        if self.ended == '' or self.ended == None:
            messages.append("Не была выбрана дата окончания")
            context['error'] = True
        else:
            try:
                self.ended = datetime.datetime.strptime(self.ended , "%Y-%m-%d").date()
                self.started = datetime.datetime.strptime(self.started , "%Y-%m-%d").date()
            except:
                messages.append("Формат данных начала и конца рассылки не подлежит конвертации в date")
                context['error'] = True
                self.ended = datetime.date.today()
                self.started = datetime.date.today()
            if (self.ended <= datetime.date.today()):
                messages.append("Дата окончания рассылки должен быть позже сегоднешнего числа")
                context['error'] = True
            if (self.ended <= self.started):
                messages.append("Дата окончания рассылки должен быть позже даты начала рассылки")
                context['error'] = True
        if (len(self.text) < 20):
            messages.append("Количество символов в тексте письма должно быть больше 20 на данный момент: " + str(len(self.text)))
            context['error'] = True
        if (len(self.filters) == 0):
            messages.append("Должны быть выбраны фильтры для рассылки")
            context['error'] = True
        else:
            for filter in self.filters:
                if Filter.objects.filter(id = filter).get():
                    pass
                else:
                    messages.append("Выбранный фильтр не был найден, обновите страницу и создайте снова")
                    context['error'] = True
                    break

        context['messages'] = messages

        return context