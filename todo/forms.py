from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Form, EmailField, EmailInput, CharField, PasswordInput, Textarea, DateTimeInput, Select, ModelForm, TextInput, ChoiceField, FileInput
from .models import Task, Comment

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "descriptions", "deadline", "priority", "status"]
        widgets = {
            "title": TextInput(attrs={
                'placeholder': 'Назва завдання',
                'class': 'form-control',
                'style': 'background-color: #f7decdeb;'
            }),
            "descriptions": Textarea(attrs={
                'placeholder': 'Опис завдання',
                'class': 'form-control',
                'style': 'background-color: #f7decdeb;'
            }),
            "deadline": DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'Дедлайн',
                'style': 'background-color: #f7decdeb;'
            }),
            "priority": Select(attrs={
                'style': 'background-color: #f7decdeb;',
                'class': 'form-control',
            }),
            "status": Select(attrs={
                'style': 'background-color: #f7decdeb;',
                'class': 'form-control',
            }),
            # "created_by": Select(attrs={
            #     'style': 'background-color: #f7decdeb; pointer-events: none;',
            #     'class': 'form-control',
            # })
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text", "media"]
        widgets = {
            "text": Textarea(attrs={
                'class': 'form-control custom-text-input',
                'placeholder': 'Ваш коментар',

            }),
            'media': FileInput(attrs={
                'class': 'custom-file-input',
                'id': 'media',
                'accept': 'image/*'
            })
        }

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control-my form-control email',
                'placeholder': 'Імя користувача',
                'style': 'background-color: #f7decdeb; '
            }),
            "email": EmailInput(attrs={
                'class': 'form-control-my form-control email',
                'placeholder': 'Ваша пошта',
                'style': 'background-color: #f7decdeb;'
            }),
            "password1": PasswordInput(attrs={
                'class': 'form-control-my form-control',
                'placeholder': 'Придумайте пароль',
            }),
            "password2": PasswordInput(attrs={
                'class': 'form-control-my form-control',
                'placeholder': 'Повторіть пароль'
            })
        }

class EmailPasswordForm(Form):
    email = EmailField(
        label="Електронна пошта", 
        widget=EmailInput(attrs={
            'class': 'form-control-my form-control email',
            'placeholder': 'Ваша пошта',
            'style': 'background-color: #f7decdeb;'
        })
    )
    password = CharField(
        widget=PasswordInput(attrs={
            'class': 'form-control-my form-control email',
            'placeholder': 'Пароль',
            'style': 'background-color: #f7decdeb;'
        }),
        label="Пароль"
    )

class TaskFilterForm(Form):
    STATUS_CHOICES = [
        ('', 'Всі'),
        ('to_do', 'Зробити'),
        ('in_progress', 'В процесі'),
        ('done', 'Готово'),
    ]
    PRIORITY_CHOICES = [
        ('', 'Всі'),
        ('low', 'Маленький'),
        ('medium', 'Середній'),
        ('high', 'Великий'),
    ]
    status = ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        label='Статус',
        widget=Select(attrs={
            'onchange': "document.getElementById('statusForm').submit()",
            'style': "background-color: #f7decdeb; border-radius: 10px; border-color: #d4b19aeb;",
            'class': 'form-select'
        }))

    priority = ChoiceField(
        choices=PRIORITY_CHOICES,
        required=False,
        label='Приорітет')

    def __init__(self, *args, **kwargs):
        super(TaskFilterForm, self).__init__(*args, **kwargs)
        self.fields['priority'].widget.attrs.update({
            'onchange': "document.getElementById('priorityForm').submit()",
            'style': "background-color: #f7decdeb; border-radius: 10px; border-color: #d4b19aeb;",
            'class': 'form-select'
            }),
        self.fields['status'].widget.attrs.update({
            'onchange': "document.getElementById('statusForm').submit()",
            'style': "background-color: #f7decdeb; border-radius: 10px; border-color: #d4b19aeb;",
            'class': 'form-select'
            })


