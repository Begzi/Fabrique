# Fabrique
Зависимости для данного проекта
bx-py-utils     68
Django          4.1
django-seed     0.3.1
django-tools    0.53.0
psycopg2        2.9.3

Либо есть txt файл, в котором есть все зависимости моего проекта.
Было сделано из тестового задания (https://www.craft.do/s/n6OVYFVUpq0o6L) "Спроектировать и реализовать API для":
•
добавления нового клиента в справочник со всеми его атрибутами
•
обновления данных атрибутов клиента
•
удаления клиента из справочника
•
добавления новой рассылки со всеми её атрибутами
•
получения общей статистики по созданным рассылкам и количеству отправленных сообщений по ним с группировкой по статусам
•
получения детальной статистики отправленных сообщений по конкретной рассылке
•
обновления атрибутов рассылки
•
удаления рассылки

4 приложения, main, client, notice, message(ничего на данный момент не далает так как не сделал отправку API на внешнего сервиса отправки).
Рассылка должна иметь фильтры по которым можно отправлять клиентам, поэтому было сделано связь многое ко многим, у моделей Filter -> Notice, через вспомогательный модель Notice_filter.

Маршрутизация, пример Notice(Рассылки)
app_name = 'notice'
urlpatterns = [
    path('', index, name = 'index'),  
    path('create', create, name = 'create'),
    path('storage', storage, name = 'storage'),
    path('edit<int:notice_id>', edit, name = 'edit'),
    path('update<int:notice_id>', update, name = 'update'),
    path('delete<int:notice_id>', delete, name = 'delete'),
    path('api/show', GetNoticeInfoView.as_view()),
    path('api/create', GetNoticeWriteInfoView.as_view()),
    path('api/edit<int:id>', GetNoticeEditInfoView.as_view()),
    path('api/delete<int:id>', GetNoticeEditInfoView.as_view()),
    path('api/view<int:id>', GetNoticeViewInfoView.as_view()),
]
