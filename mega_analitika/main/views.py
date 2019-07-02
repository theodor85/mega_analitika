from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import EnterTaskForm


class MainView(FormView):
    template_name = 'main/main.html'
    form_class = EnterTaskForm