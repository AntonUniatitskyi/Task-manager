from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from todo import models
from .forms import UserForm, EmailPasswordForm, TaskForm, TaskFilterForm, CommentForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import UserIsOwnerMixin
from django.http import HttpResponseRedirect

# Create your views here.

class TaskListView(ListView):
    model = models.Task
    template_name = 'todo/tasks.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get("status", "")
        priority = self.request.GET.get("priority", "")
        user = self.request.session.get('username')
        if user:
            queryset = queryset.filter(created_by__username=user)
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskFilterForm(self.request.GET)
        return context


class TaskListDetail(UserIsOwnerMixin, DetailView):
    model = models.Task
    template_name = 'todo/task_detail.html'
    context_object_name = 'task_detail'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


    def post(self, request, *args, **kwargs):
        task = self.get_object()
        new_status = request.POST.get('status')

        if new_status in dict(task.STATUS_CHOICES):
            task.status = new_status
            task.save()
            return redirect('task_detail', pk=task.pk)

        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.creator = request.user
            comment.save()
            return redirect('task_detail', pk=task.pk)

        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)



def logout_view(request):
    logout(request)
    return redirect('task_list')

def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                request.session['username'] = user.username
                messages.success(request, 'Користувач успішно створений!')
                return redirect('task_list')
            except IntegrityError:
                messages.error(request, 'Користувач з такою поштою вже зареєстрований.')
        else:
            print(form.errors)
            messages.error(request, 'Виникла помилка. Перевірте введені дані.')
    else:
        form = UserForm()
    
    return render(request, 'todo/create_user.html', {'form': form})


def request_login(request):
    if request.method == 'POST':
        form = EmailPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Перевірка користувача
            try:
                admin = User.objects.get(email=email)
                if admin.check_password(password):
                    login(request, admin)
                    request.session['username'] = admin.username
                    messages.success(request, 'Ви успішно увійшли як адмін!')
                    return redirect('task_list')
                else:
                    messages.error(request, 'Невірний пароль!')
                    return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'Користувач або адмін з таким email не знайдено.')
                return redirect('login')

    else:
        form = EmailPasswordForm()
    return render(request, 'todo/request_login.html', {'form': form})

class CreateTaskView(LoginRequiredMixin, CreateView):
    model = models.Task
    template_name = "todo/add_task.html"
    form_class = TaskForm
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class TaskCompleteView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = 'done'
        task.save()

        return HttpResponseRedirect(reverse_lazy('task_list'))
    
    def get_object(self):
        task_id = self.kwargs.get('pk')
        return get_object_or_404(models.Task, pk=task_id)
    
class UpdateTaskView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = models.Task
    form_class = TaskForm
    template_name = "todo/task_update_form.html"
    success_url = reverse_lazy('task_list')

class DeleteTaskView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = models.Task
    template_name = "todo/delete_task_form.html"
    success_url = reverse_lazy('task_list')