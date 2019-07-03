from __future__ import absolute_import, unicode_literals
from datetime import time, date

from celery import shared_task

from .models import Task
from .scrap import scrap_data


def write_to_DB(task_pk, data):
    task = Task(pk=task_pk)
    for item in data:
        print(item[0], item[1])


@shared_task
def scrap_data_and_write_to_DB(task_pk, url):
    data = scrap_data(url)
    write_to_DB(task_pk, data)