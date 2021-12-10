from django import forms
from django.contrib.auth.models import User
from . import models



#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


#for student related form
class EmployeeUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class EmployeeForm(forms.ModelForm):
    class Meta:
        model=models.Employee
        fields=['mobile','department','status']



class TaskForm(forms.ModelForm):
    #this is the extrafield for linking task and their assigend employee
    #this will show dropdown __str__ method employee model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in Employee model and return it
    assignedEmployeeId=forms.ModelChoiceField(queryset=models.Employee.objects.all(),empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Task
        fields=['taskTitle','description','deadlineDate','status']



class ScheduleForm(forms.ModelForm):
    taskId=forms.ModelChoiceField(queryset=models.Task.objects.all().filter(status=True),empty_label="Task Title and Description", to_field_name="id")
    employeeId=forms.ModelChoiceField(queryset=models.Employee.objects.all().filter(status=True),empty_label="Employee Name and Department", to_field_name="id")
    class Meta:
        model=models.Schedule
        fields=['scheduleStart','scheduleFinish','scheduleInfo','status']


class TaskScheduleForm(forms.ModelForm):
    employeeId=forms.ModelChoiceField(queryset=models.Employee.objects.all().filter(status=True),empty_label="Employee Name and Department", to_field_name="id")
    class Meta:
        model=models.Schedule
        fields=['scheduleInfo','status']


