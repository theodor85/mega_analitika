from django.shortcuts import render
from django.views.generic.base import View
from django.contrib import messages

from .forms import EnterTaskForm
from .functions import execute_task


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