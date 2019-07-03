from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.contrib import messages

from .forms import EnterTaskForm
from .functions import execute_task
from .models import Task, PopularDay, PopularTime


class MainView(View):
    
    def get(self, request):
        form = EnterTaskForm()
        return render(request, 'main/main.html', {'form': form})

    def post(self, request):
        form = EnterTaskForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            email = form.cleaned_data['email']
            description = form.cleaned_data['description']

            execute_task(url, email, description)

            messages.add_message(request, messages.SUCCESS, 
                'Задание принято!')
            return render(request, 'main/main.html', {'form': form})

        messages.add_message(request, messages.WARNING, 
                'Задание не принято и не будет выполнено!')
        return render(request, 'main/main.html', {'form': form})


class ReportView(View):
    def get(self, request):

        if request.GET['task']:
            task_pk = request.GET['task']
        else:
            return render(request, 'main/empty.html')

        task = get_object_or_404(Task, pk = task_pk)
        pds = PopularDay.objects.filter(task=task).all()
        dic_days = {pd.day: pd.counter for pd in pds}
        lst_days = [ dic_days.get(i, 0) for i in range(1, 8)]

        pts = PopularTime.objects.filter(task=task).all()
        dic_time = {pt.time: pt.counter for pt in pts}
        lst_time = [ dic_days.get(i, 0) for i in range(24)]

        context = {
            'title': 'Это ваш отчет!',
            'description': task.description,
            'data_days': lst_days,
            'data_time': lst_time,
        }
        return render(request, 'main/report.html', context)