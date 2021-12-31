from django.urls import path
from . import views

urlpatterns = [
    path('', views.backlog, name='backlog'),
    path('weeks', views.weeksbacklog, name='weeks'),
    path('cmunit/<dept>', views.cm_units, name='cmunit'),
    path('weeksunit/<dept>', views.weeks_units, name='weeksunit')
    
]