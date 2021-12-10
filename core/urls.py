"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from runsheet import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),


    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),


    path('adminclick', views.adminclick_view),
    path('employeeclick', views.employeeclick_view),
    path('taskclick', views.taskclick_view),

    path('adminsignup', views.admin_signup_view),
    path('employeesignup', views.employee_signup_view,name='employeesignup'),
    path('tasksignup', views.task_signup_view),
    
    path('adminlogin', LoginView.as_view(template_name='runsheet/adminlogin.html')),
    path('employeelogin', LoginView.as_view(template_name='runsheet/employeelogin.html')),
    path('tasklogin', LoginView.as_view(template_name='runsheet/tasklogin.html')),


    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='runsheet/index.html'),name='logout'),


    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-employee', views.admin_employee_view,name='admin-employee'),
    path('admin-view-employee', views.admin_view_employee_view,name='admin-view-employee'),
    path('delete-employee-from-runsheet/<int:pk>', views.delete_employee_from_runsheet_view,name='delete-employee-from-runsheet'),
    path('update-employee/<int:pk>', views.update_employee_view,name='update-employee'),
    path('admin-add-employee', views.admin_add_employee_view,name='admin-add-employee'),
    path('admin-approve-employee', views.admin_approve_employee_view,name='admin-approve-employee'),
    path('approve-employee/<int:pk>', views.approve_employee_view,name='approve-employee'),
    path('reject-employee/<int:pk>', views.reject_employee_view,name='reject-employee'),
    path('admin-view-employee-specialisation',views.admin_view_employee_specialisation_view,name='admin-view-employee-specialisation'),


    path('admin-task', views.admin_task_view,name='admin-task'),
    path('admin-view-task', views.admin_view_task_view,name='admin-view-task'),
    path('delete-task-from-runsheet/<int:pk>', views.delete_task_from_runsheet_view,name='delete-task-from-runsheet'),
    path('update-task/<int:pk>', views.update_task_view,name='update-task'),
    path('admin-add-task', views.admin_add_task_view,name='admin-add-task'),
    path('admin-approve-task', views.admin_approve_task_view,name='admin-approve-task'),
    path('approve-task/<int:pk>', views.approve_task_view,name='approve-task'),
    path('reject-task/<int:pk>', views.reject_task_view,name='reject-task'),
    path('admin-complete-task', views.admin_complete_task_view,name='admin-complete-task'),
    path('complete-task/<int:pk>', views.complete_task_view,name='complete-task'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),


    path('admin-schedule', views.admin_schedule_view,name='admin-schedule'),
    path('admin-view-schedule', views.admin_view_schedule_view,name='admin-view-schedule'),
    path('admin-add-schedule', views.admin_add_schedule_view,name='admin-add-schedule'),
    path('admin-approve-schedule', views.admin_approve_schedule_view,name='admin-approve-schedule'),
    path('approve-schedule/<int:pk>', views.approve_schedule_view,name='approve-schedule'),
    path('reject-schedule/<int:pk>', views.reject_schedule_view,name='reject-schedule'),
    path('delete-schedule-from-runsheet/<int:pk>', views.delete_schedule_from_runsheet_view,name='delete-schedule-from-runsheet'),
]


#---------FOR EMPLOYEE RELATED URLS-------------------------------------
urlpatterns +=[
    path('employee-dashboard', views.employee_dashboard_view,name='employee-dashboard'),
    path('search', views.search_view,name='search'),

    path('employee-task', views.employee_task_view,name='employee-task'),
    path('employee-view-task', views.employee_view_task_view,name='employee-view-task'),
    path('employee-view-complete-task',views.employee_view_complete_task_view,name='employee-view-complete-task'),

    path('employee-schedule', views.employee_schedule_view,name='employee-schedule'),
    path('employee-view-schedule', views.employee_view_schedule_view,name='employee-view-schedule'),
    path('employee-delete-schedule',views.employee_delete_schedule_view,name='employee-delete-schedule'),
    path('delete-schedule/<int:pk>', views.delete_schedule_view,name='delete-schedule'),
]




#---------FOR TASK RELATED URLS-------------------------------------
urlpatterns +=[

    path('task-dashboard', views.task_dashboard_view,name='task-dashboard'),
    path('task-schedule', views.task_schedule_view,name='task-schedule'),
    path('task-book-schedule', views.task_book_schedule_view,name='task-book-schedule'),
    path('task-view-schedule', views.task_view_schedule_view,name='task-view-schedule'),
    path('task-view-employee', views.task_view_employee_view,name='task-view-employee'),
    path('searchemployee', views.search_employee_view,name='searchemployee'),
    path('task-complete', views.task_complete_view,name='task-complete'),

]
