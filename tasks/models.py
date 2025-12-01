from django.db import models
from django.db.models.signals import post_save,pre_save,m2m_changed,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User

# Create your models here.

# if project not defined then use double quotation or bring the parent table on top of child

class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING','Pending'),
        ('IN_PROGRESS','In Progress'),
        ('COMPLETED','Completed')
    ]
    project = models.ForeignKey("Project", on_delete=models.CASCADE,default=1)
    # assigned_to = models.ManyToManyField(Employee, related_name='tasks')
    assigned_to = models.ManyToManyField(User, related_name='tasks')
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status  = models.CharField(max_length=15, choices=STATUS_CHOICES,default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'

    PRIORITY_OPTIONS = (
        (HIGH,'High'),
        (MEDIUM, 'Medium'),
        (LOW,'Low')
    )
    # std_id = models.CharField(max_length=200,primary_key=True)
    task = models.OneToOneField(
        Task, 
        on_delete = models.DO_NOTHING,
        related_name="details"
    )
    asset = models.ImageField(upload_to='tasks_asset',blank=True,null=True)
    priority = models.CharField(max_length=1,choices = PRIORITY_OPTIONS,default=LOW)
    notes = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"Details form Task {self.task.title}"

# Task.objcets.get(id=2)
# select * from task where id = 2
# ORM = object relational mapper

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    start_date = models.DateField()

    def __str__(self):
        return self.name
