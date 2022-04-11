from django.db import models
from django.contrib.auth.models import User



departments=[('Administrator','Administrator'),
('IT Support','IT Support'),
]
class Employee(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Administrator')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)



class Task(models.Model):
    assignedEmployeeId = models.PositiveIntegerField(null=True)
    taskTitle=models.CharField(max_length=70)
    description=models.TextField(max_length=500)
    assignDate=models.DateField(auto_now=True)
    deadlineDate=models.DateField(null=False)
    status=models.BooleanField(default=False)
    def __str__(self):
        return "{} ({})".format(self.taskTitle,self.deadlineDate)


class Schedule(models.Model):
    taskId=models.PositiveIntegerField(null=True)
    employeeId=models.PositiveIntegerField(null=True)
    scheduleStart=models.DateTimeField(null=False)
    scheduleFinish=models.DateTimeField(null=False)
    scheduleInfo=models.TextField(max_length=500)
    status=models.BooleanField(default=False)

    
    def employeeName(self):
        emp = Employee.objects.get(id=self.employeeId)
        name = emp.mobile
        return "test"+name
        return Employee.get_name(emp)



class TaskCompleteDetails(models.Model):
    taskId=models.PositiveIntegerField(null=True)
    taskTitle=models.CharField(max_length=40)
    assignedEmployeeName=models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)

    assignDate=models.DateField(null=False)
    deadlineDate=models.DateField(null=False)

    description=models.TextField(max_length=500)
    comment=models.TextField(max_length=500,null=True)
    pdf=models.FileField(upload_to='pdfs/')
    status=models.BooleanField(default=False)


