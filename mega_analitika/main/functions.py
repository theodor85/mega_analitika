from .models import Task
from .tasks import scrap_data_and_get_statistic

def execute_task(url, email, description):
    # сохранить задачу
    task = Task()
    task.description = description 
    task.email = email
    task.save()
    # запустить celery
    start_celery_task(task, url)


def start_celery_task(task, url):
    scrap_data_and_get_statistic.delay(task.pk, url)