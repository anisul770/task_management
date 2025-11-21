from django.urls import path
from tasks.views import manager_dashboard,employee_dashboard,create_task,view_task, update_task,delete_task

urlpatterns = [
    path('manager_dashboard/',manager_dashboard, name = "manager-dashboard"),
    path('user_dashboard/',employee_dashboard, name = "user-dashboard"),
    path('create_task/',create_task, name = 'create-task'),
    path('view_task/',view_task),
    path('update_task/<int:id>/',update_task, name = 'update-task'),
    path('delete_task/<int:id>/',delete_task, name = 'delete-task')
]