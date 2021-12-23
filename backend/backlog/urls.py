from django.urls import path
from . import views

urlpatterns = [
    path('', views.backlog, name='backlog'),
    path('weeks', views.weeksbacklog, name='weeks'),
    path('deptbacklog/<dept>', views.dept_backlog, name='deptbacklog'),
    
]