from __future__ import absolute_import, unicode_literals
from datetime import time, date
from collections import Counter

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from celery import shared_task

from .models import Task, PopularDay, PopularTime
from .scrap import scrap_data


def write_to_DB(task_pk, counters):
    task = Task(pk=task_pk)
    # сохраням дни недели
    for day, count in counters[0].items():
        pd = PopularDay()
        pd.task = task
        pd.day = day
        pd.counter = count
        pd.save()
    # сохраняем часы
    for hour, count in counters[1].items():
        pt = PopularTime()
        pt.task = task
        pt.time = hour
        pt.counter = count
        pt.save()


def pickup_statistic(data):
    hours_counter = Counter()
    days_counter = Counter()
    for item in data:
        hours_counter.update( (item[1].hour, ) )
        days_counter.update( (item[0].weekday()+1, ) )
    return (days_counter, hours_counter)


def pickup_statistic_and_write_to_DB(task_pk, data):
    counters = pickup_statistic(data)
    write_to_DB(task_pk, counters)


def send_email_notification(task_pk):
    task = Task(pk=task_pk)

    if settings.ALLOWED_HOSTS:
        host = 'http://' + settings.ALLOWED_HOSTS[0] + ':8000'
    else:
        host = 'http://0.0.0.0:8000'

    context = {'task_pk': task_pk, 'host': host }
    body_mail = render_to_string('main/letter.txt', context)
    subj = 'Ссылка на отчет по сайту olx.ua'
    mailer = EmailMessage(subject=subj, body=body_mail, to=[task.email])
    mailer.send()

@shared_task
def scrap_data_and_get_statistic(task_pk, url):
    data = scrap_data(url)
    pickup_statistic_and_write_to_DB(task_pk, data)
    send_email_notification(task_pk)
    