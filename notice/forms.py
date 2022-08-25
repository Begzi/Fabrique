
from .models import Filter

import datetime




class NoticeValid:
    def __init__(self, ended, text, filters):

        self.ended = ended
        self.text = text
        if filters is None:
            filters = []
        self.filters = filters
    def is_valid(self):
        context = {'error' : False }
        messages = []
        if self.ended == '' or self.ended == None:
            messages.append("Не была выбрана дата окончания")
            context['error'] = True
        else:
            if (datetime.datetime.strptime(self.ended , "%Y-%m-%d").date() <= datetime.date.today()):
                messages.append("Не корректная дата окончания рассылки")
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