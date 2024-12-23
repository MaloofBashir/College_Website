from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Table_rollno/', views.Table_rollno, name='Table_rollno'),
    path('export_excel/', views.export_excel, name='export_excel'),
]
