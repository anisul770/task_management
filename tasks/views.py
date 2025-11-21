from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm,TaskDetailModelForm
from tasks.models import Employee,Task,TaskDetail,Project
from datetime import date
from django.db.models import Q,Count,Max,Min
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test,login_required,permission_required

# Create your views here.

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='Employee').exists()

@user_passes_test(is_manager,login_url='no-permission')
def manager_dashboard(request):
    type = request.GET.get('type','all')
    print(type)
    

    counts = Task.objects.aggregate(total = Count('id'), completed = Count('id',filter = Q(status='COMPLETED')),in_progress = Count('id',filter = Q(status='IN_PROGRESS')),pending = Count('id',filter = Q(status='PENDING')))

    # Retrieving task data

    base_query = Task.objects.select_related("details").prefetch_related('assigned_to')

    if type == 'completed':
        tasks = base_query.filter(status = 'COMPLETED')
    elif type == 'in-progress':
        tasks = base_query.filter(status = 'IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status = 'PENDING')
    elif type == 'all':
        tasks = base_query.all()

    context = {
        "tasks" : tasks,
        "counts" : counts
    }
    return render(request,"dashboard/manager_dashboard.html",context)

# CRUD
# C = CREATE
# R = READ
# U = UPDATE
# D = DELETE

@user_passes_test(is_employee,login_url='no-permission')
def employee_dashboard(request):
    return render(request,"dashboard/user_dashboard.html")

@login_required
@permission_required("task.add_task",login_url='no-permission')
def create_task(request):
    # employees = Employee.objects.all()
    task_form = TaskModelForm() # by default GET
    task_detailed_form = TaskDetailModelForm()
    if request.method == "POST":
        task_form = TaskModelForm(request.POST)
        task_detailed_form = TaskDetailModelForm(request.POST)
        if task_form.is_valid() and task_detailed_form.is_valid():
            """For Model Form Data"""

            task = task_form.save()
            task_detail = task_detailed_form.save(commit = False)
            task_detail.task = task
            task_detail.save()

            messages.success(request,"Task Created Successfully")
            return redirect('create-task')

            '''For Django Form Data'''
            # data = form.cleaned_data
            # title = data.get('title')      
            # description = data.get("description")
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to')

            # task = Task.objects.create(
            #     title = title, description = description,due_date = due_date
            # )

            # # assign employee to task
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id = emp_id)
            #     task.assigned_to.add(employee)
    
            # return HttpResponse("Task Added Successfully")
    context = {
        "task_form": task_form,
        "task_detail_form" : task_detailed_form
    }
    return render(request,"task_form.html",context)

@login_required
@permission_required("task.change_task",login_url='no-permission')
def update_task(request,id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task) # by default GET
    if task.details:
        task_detailed_form = TaskDetailModelForm(instance=task.details)
    if request.method == "POST":
        task_form = TaskModelForm(request.POST,instance=task)
        task_detailed_form = TaskDetailModelForm(request.POST,instance=task.details)
        if task_form.is_valid() and task_detailed_form.is_valid():
            """For Model Form Data"""

            task = task_form.save()
            task_detail = task_detailed_form.save(commit = False)
            task_detail.task = task
            task_detail.save()

            messages.success(request,"Task Updated Successfully")
            return redirect('update-task',id)

            '''For Django Form Data'''
            # data = form.cleaned_data
            # title = data.get('title')      
            # description = data.get("description")
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to')

            # task = Task.objects.create(
            #     title = title, description = description,due_date = due_date
            # )

            # # assign employee to task
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id = emp_id)
            #     task.assigned_to.add(employee)
    
            # return HttpResponse("Task Added Successfully")
    context = {
        "task_form": task_form,
        "task_detail_form" : task_detailed_form
    }
    return render(request,"task_form.html",context)

@login_required
@permission_required("task.delete_task",login_url='no-permission')
def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        print(f'Got the task {task}')
        messages.success(request,"Task Deleted Successfully")
        return redirect('manager-dashboard')
    else:
        messages.error(request,"Something went wrong")
        return redirect('manager-dashboard')

@login_required
@permission_required("task.view_task",login_url='no-permission')
def view_task(request):
    # retrieve all data from tasks model
    # tasks = Task.objects.all()

    #retrieve a specific task
    #task_3 = Task.objects.first()

    # Filter ew
    #pending_task = Task.objects.filter(status = "PENDING") 

    #show task  which due date is today
    #tasks = Task.objects.filter(due_date = date.today())

    """Show the task whose priority is not low"""
    # tasks = TaskDetail.objects.exclude(priority = 'H')

    """Show the task that contain word 'cup'"""
    # tasks = Task.objects.filter(title__icontains = "Cup")

    """Show the task that contain word 'cup'"""
    # tasks = Task.objects.filter(Q(status = "PENDING") | Q(status = "IN_PROGRESS"))

    # tasks = Task.objects.filter(status = "jhsfdg").exists()

    # select_related(ForeignKey, OneToOneField)
    # tasks = Task.objects.all()

    #access with task table
    # tasks = Task.objects.select_related("details").all()

    # tasks = TaskDetail.objects.select_related("task").all()

    # tasks = Task.objects.select_related("project").all()

    '''prefetch_related (reverse ForeignKey, manytomany)'''
    # tasks = Project.objects.prefetch_related("task_set").all()
    # tasks = Task.objects.prefetch_related("assigned_to").all()

    '''aggregate'''
    # task_count = Task.objects.aggregate(num_task=Count('id'))
    # task_count = Project.objects.annotate(num_task=Count('task')).order_by('num_task')
    # projects_without_tasks = Project.objects.filter(task__isnull=True)
    emp = Employee.objects.annotate(no_task = Count("tasks"))
    return render(request,"show_task.html",{"tsk_count":emp})