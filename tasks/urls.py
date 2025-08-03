from django.urls import path
from tasks.views import manager_dashboard,user_dashboard,test

urlpatterns = [
    path('manager_dashboard/',manager_dashboard),
    path('user_dashboard/',user_dashboard),
    path('test/',test),
]