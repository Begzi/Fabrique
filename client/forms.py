from .models import TimeZone

class ClientValid:
    def __init__(self, phone, code, tag, time_zone_id):
        self.phone = phone
        self.code = code
        self.tag = tag
        self.time_zone_id = time_zone_id

    def is_valid(self):
        context = {'error' : False }
        messages = []
        if self.phone == '' or self.phone == None:
            messages.append("Не ввели номер телефона")
            context['error'] = True
        else:
            if (len(self.phone) != 12):
                messages.append("Номер телефона должен быть равен 12 символов")

        if self.code == '' or self.code == None:
            messages.append("Не ввели Код мобильного оператора")
            context['error'] = True
        else:
            if (len(self.code) > 5):
                messages.append("Код мобильного оператора не должен быть больше 5 символов")

        if self.tag == '' or self.tag == None:
            messages.append("Не ввели тег")
            context['error'] = True
        else:
            if (len(self.tag) > 12):
                messages.append("Тег не должен быть больше 15 символов")
                context['error'] = True

        if TimeZone.objects.filter(id = self.time_zone_id).get():
            pass
        else:
            messages.append("Выбранный часовой пояс не был найден, обновите страницу и попытайтесь заного")
            context['error'] = True


        context['messages'] = messages

        return context