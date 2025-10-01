from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee,Task,TaskDetail,Project
from datetime import date
from django.db.models import Q,Count,Max,Min

# Create your views here.

def manager_dashboard(request):
    return render(request,"dashboard/manager_dashboard.html")

def user_dashboard(request):
    return render(request,"dashboard/user_dashboard.html")

def test(request):
    names = ["Mahmud", "Ahamed","John","Fahim"]
    count = 0
    for name in names:
      count+=1
    context = {
        "names" : names,
        "age" : 23,
        "count" : count
    }
    return render(request,'test.html',context)

def create_task(request):
    # employees = Employee.objects.all()
    form = TaskModelForm() # by default GET
    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():
            """For Model Form Data"""

            form.save()
            return render(request,'task_form.html',{"form": form,"message":"task added successfully"})

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
    
            return HttpResponse("Task Added Successfully")
    context = {
        "form": form
    }
    return render(request,"task_form.html",context)

def view_task(request):
    # retrieve all data from tasks model
    # tasks = Task.objects.all()

    #retrieve a specific task
    #task_3 = Task.objects.first()

    # Filter 
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
    task_count = Project.objects.annotate(num_task=Count('task')).order_by('num_task')
    return render(request,"show_task.html",{"tsk_count":task_count})