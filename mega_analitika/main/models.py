from django.db import models


class Task(models.Model):
    ''' Задача сбора информации '''
    description = models.TextField(verbose_name='Описание задачи', 
        help_text='Это описание будет использовано в заголовке отчета')
    email = models.EmailField(verbose_name='Email', 
        default='fedor_coder@mail.ru')


class PopularTime(models.Model):
    ''' Эта таблица вычисляется на основе данных, сграбленных с сайта. 
    Фактически, это готовый отчет, который можно выводить пользователю. '''
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    time = models.SmallIntegerField()
    counter = models.IntegerField()

    class Meta:
        unique_together = ('task', 'time')


class PopularDay(models.Model):
    ''' То же самое, что и PopularTime, только под дням недели. '''
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    day = models.SmallIntegerField()
    counter = models.IntegerField()
        
    class Meta:
        unique_together = ('task', 'day')