from django import forms
from django.forms.widgets import EmailInput, URLInput, TextInput
from django.core import validators

class EnterTaskForm(forms.Form):
    ''' Форма для ввода задания '''
    url = forms.URLField(label='URL', 
        help_text='Ссылка на раздел сайта www.olx.ua',
        widget = URLInput(attrs={'class':'form-control'}),
        validators = [ validators.RegexValidator( r'^https://www.olx.ua/[a-z\-]{1,}/[a-z\-]{1,}/' ) ],
        error_messages = {'invalid': 'Нужно указать ссылку на существующий раздел сайта olx.ua!'}
        )

    email = forms.EmailField(label='E-mail', 
        help_text='Ваш E-mail, на который будет выслана ссылка с отчетом',
        widget = EmailInput(attrs={'class':'form-control'}))

    description = forms.CharField(max_length=250, label='Описание',
        help_text='Это описание будет использовано в заголовке отчёта',
        widget = TextInput(attrs={'class':'form-control'}))