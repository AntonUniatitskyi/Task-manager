from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('logout', views.logout_view, name='logout'),
    path('create-user', views.add_user, name='add_user'),
    path('login', views.request_login, name='login'),
    path('task-detail-<int:pk>/', views.TaskListDetail.as_view(), name='task_detail'),
    path('new-task', views.CreateTaskView.as_view(), name='add_task'),
    path('<int:pk>/complete', views.TaskCompleteView.as_view(), name='task_complete'),
    path('task-update/<int:pk>/', views.UpdateTaskView.as_view(), name='task_update'),
    path('task-delete/<int:pk>/', views.DeleteTaskView.as_view(), name='task_delete'),
    path("approve-task/", views.ApproveTaskView.as_view(), name="approve_task"),

]