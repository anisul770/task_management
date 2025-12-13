from django.urls import path
from tasks.views import manager_dashboard,employee_dashboard,create_task,view_task, update_task,delete_task,task_details,dashboard,Greetings,HiGreetings,HiHowGreetings,CreateTask,UpdateTask,ViewProject,TaskDetail,DeleteTask,ManagerDashboard,EmployeeDashboard

urlpatterns = [
    # path('manager_dashboard/',manager_dashboard, name = "manager-dashboard"),
    path('manager_dashboard/',ManagerDashboard.as_view(), name = "manager-dashboard"),
    # path('user_dashboard/',employee_dashboard, name = "user-dashboard"),
    path('user_dashboard/',EmployeeDashboard.as_view(), name = "user-dashboard"),
    # path('create_task/',create_task, name = 'create-task'),
    path('create_task/',CreateTask.as_view(), name = 'create-task'),
    # path('view_task/',view_task,name='view-task'),
    path('view_task/',ViewProject.as_view(),name='view-task'),
    # path('task/<int:task_id>/details/',task_details,name='task-details'),
    path('task/<int:task_id>/details/',TaskDetail.as_view(),name='task-details'), #<int:pk> by default it access as pk
    # path('update_task/<int:id>/',update_task, name = 'update-task'),
    path('update_task/<int:id>/',UpdateTask.as_view(), name = 'update-task'),
    # path('delete_task/<int:id>/',delete_task, name = 'delete-task'),
    path('delete_task/<int:id>/',DeleteTask.as_view(), name = 'delete-task'),
    path('dashboard',dashboard,name='dashboard'),
    path('greetings/',HiHowGreetings.as_view(greetings="Hi Good Day"),name='greetings')
]