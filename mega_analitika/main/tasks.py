from __future__ import absolute_import, unicode_literals
from datetime import time, date

from celery import shared_task

from .models import Ad, Task


def get_data_from_site(url):
    return (
        ( time(12, 34, 50), date(2018, 6, 6) ),
        ( time(12, 34, 50), date(2018, 6, 13) ),
        ( time(8, 34, 50), date(2018, 6, 24) ),
        ( time(15, 34, 50), date(2018, 6, 25) ),
    )


def write_to_DB(task_pk, data):
    task = Task(pk=task_pk)
    for item in data:
        ad = Ad()
        ad.task = task
        ad.time = item[0]
        ad.date = item[1]
        ad.save()


@shared_task
def scrap_data_and_write_to_DB(task_pk, url):
    data = get_data_from_site(url)
    write_to_DB(task_pk, data)