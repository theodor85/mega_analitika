from django.db import models


class Task(models.Model):
    ''' Задача сбора информации '''
    description = models.TextField(verbose_name='Описание задачи', 
        help_text='Это описание будет использовано в заголовке отчета')
    email = models.EmailField(verbose_name='Email', 
        default='fedor_coder@mail.ru')


class PopularTime(models.Model):
    ''' Эта таблица вычисляется на основе данных, сохраненных в модели Ad. 
    Фактически, это готовый отчет, который можно выводить пользователю. '''
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    hours = (
        (0, '0:00'), (1, '1:00'), (2, '2:00'), (3, '3:00'), (4, '4:00'), 
        (5, '5:00'), (6, '6:00'), (7, '7:00'), (8, '8:00'), (9, '9:00'),
        (10, '10:00'), (11, '11:00'), (12, '12:00'), (13, '13:00'),
        (14, '14:00'), (15, '15:00'), (16, '16:00'), (17, '17:00'),
        (18, '18:00'), (19, '19:00'), (20, '20:00'), (21, '21:00'),
        (22, '22:00'), (23, '23:00'),
    )
    time = models.SmallIntegerField(choices=hours)
    counter = models.IntegerField()


class PopularDay(models.Model):
    ''' То же самое, что и PopularTime, только под дням недели. '''
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    days = (
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
        (7, 'Воскресение'),
    )
    day = models.SmallIntegerField(choices=days)
    counter = models.IntegerField()    