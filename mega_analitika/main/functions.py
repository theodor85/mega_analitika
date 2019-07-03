from .models import Task
from .tasks import scrap_data_and_write_to_DB

def execute_task(url, email, description):
    # сохранить задачу
    task = Task()
    task.description = description 
    task.email = email
    task.save()
    # запустить celery
    start_celery_task(task, url)


def start_celery_task(task, url):
    scrap_data_and_write_to_DB.delay(task.pk, url)