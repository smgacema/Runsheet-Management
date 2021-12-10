from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q

# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'runsheet/index.html')


#for showing signup/login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'runsheet/adminclick.html')


#for showing signup/login button for employee(by sumit)
def employeeclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'runsheet/employeeclick.html')


#for showing signup/login button for task(by sumit)
def taskclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'runsheet/taskclick.html')




def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'runsheet/adminsignup.html',{'form':form})




def employee_signup_view(request):
    userForm=forms.EmployeeUserForm()
    employeeForm=forms.EmployeeForm()
    mydict={'userForm':userForm,'employeeForm':employeeForm}
    if request.method=='POST':
        userForm=forms.EmployeeUserForm(request.POST)
        employeeForm=forms.EmployeeForm(request.POST,request.FILES)
        if userForm.is_valid() and employeeForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            employee=employeeForm.save(commit=False)
            employee.user=user
            employee=employee.save()
            my_employee_group = Group.objects.get_or_create(name='EMPLOYEE')
            my_employee_group[0].user_set.add(user)
        return HttpResponseRedirect('employeelogin')
    return render(request,'runsheet/employeesignup.html',context=mydict)


def task_signup_view(request):
    userForm=forms.TaskUserForm()
    taskForm=forms.TaskForm()
    mydict={'userForm':userForm,'taskForm':taskForm}
    if request.method=='POST':
        userForm=forms.TaskUserForm(request.POST)
        taskForm=forms.TaskForm(request.POST,request.FILES)
        if userForm.is_valid() and taskForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            task=taskForm.save(commit=False)
            task.user=user
            task.assignedEmployeeId=request.POST.get('assignedEmployeeId')
            task=task.save()
            my_task_group = Group.objects.get_or_create(name='TASK')
            my_task_group[0].user_set.add(user)
        return HttpResponseRedirect('tasklogin')
    return render(request,'runsheet/tasksignup.html',context=mydict)






#-----------for checking user is employee , task or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_employee(user):
    return user.groups.filter(name='EMPLOYEE').exists()
def is_task(user):
    return user.groups.filter(name='TASK').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,EMPLOYEE OR TASK
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_employee(request.user):
        accountapproval=models.Employee.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('employee-dashboard')
        else:
            return render(request,'runsheet/employee_wait_for_approval.html')
    elif is_task(request.user):
        accountapproval=models.Task.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('task-dashboard')
        else:
            return render(request,'runsheet/task_wait_for_approval.html')








#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    employees=models.Employee.objects.all().order_by('-id')
    tasks=models.Task.objects.all().order_by('-id')
    #for three cards
    employeecount=models.Employee.objects.all().filter(status=True).count()
    pendingemployeecount=models.Employee.objects.all().filter(status=False).count()

    taskcount=models.Task.objects.all().filter(status=True).count()
    pendingtaskcount=models.Task.objects.all().filter(status=False).count()

    schedulecount=models.Schedule.objects.all().filter(status=True).count()
    pendingschedulecount=models.Schedule.objects.all().filter(status=False).count()
    mydict={
    'employees':employees,
    'tasks':tasks,
    'employeecount':employeecount,
    'pendingemployeecount':pendingemployeecount,
    'taskcount':taskcount,
    'pendingtaskcount':pendingtaskcount,
    'schedulecount':schedulecount,
    'pendingschedulecount':pendingschedulecount,
    }
    return render(request,'runsheet/admin_dashboard.html',context=mydict)


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_employee_view(request):
    return render(request,'runsheet/admin_employee.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_employee_view(request):
    employees=models.Employee.objects.all().filter(status=True)
    return render(request,'runsheet/admin_view_employee.html',{'employees':employees})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_employee_from_runsheet_view(request,pk):
    employee=models.Employee.objects.get(id=pk)
    user=models.User.objects.get(id=employee.user_id)
    user.delete()
    employee.delete()
    return redirect('admin-view-employee')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_schedule_from_runsheet_view(request,pk):
    schedule=models.Schedule.objects.get(id=pk)
    schedule.delete()
    return redirect('admin-view-schedule')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_employee_view(request,pk):
    employee=models.Employee.objects.get(id=pk)
    user=models.User.objects.get(id=employee.user_id)

    userForm=forms.EmployeeUserForm(instance=user)
    employeeForm=forms.EmployeeForm(request.FILES,instance=employee)
    mydict={'userForm':userForm,'employeeForm':employeeForm}
    if request.method=='POST':
        userForm=forms.EmployeeUserForm(request.POST,instance=user)
        employeeForm=forms.EmployeeForm(request.POST,request.FILES,instance=employee)
        if userForm.is_valid() and employeeForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            employee=employeeForm.save(commit=False)
            employee.status=True
            employee.save()
            return redirect('admin-view-employee')
    return render(request,'runsheet/admin_update_employee.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_employee_view(request):
    userForm=forms.EmployeeUserForm()
    employeeForm=forms.EmployeeForm()
    mydict={'userForm':userForm,'employeeForm':employeeForm}
    if request.method=='POST':
        userForm=forms.EmployeeUserForm(request.POST)
        employeeForm=forms.EmployeeForm(request.POST, request.FILES)
        if userForm.is_valid() and employeeForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            employee=employeeForm.save(commit=False)
            employee.user=user
            employee.status=True
            employee.save()

            my_employee_group = Group.objects.get_or_create(name='EMPLOYEE')
            my_employee_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-employee')
    return render(request,'runsheet/admin_add_employee.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_employee_view(request):
    #those whose approval are needed
    employees=models.Employee.objects.all().filter(status=False)
    return render(request,'runsheet/admin_approve_employee.html',{'employees':employees})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_employee_view(request,pk):
    employee=models.Employee.objects.get(id=pk)
    employee.status=True
    employee.save()
    return redirect(reverse('admin-approve-employee'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_employee_view(request,pk):
    employee=models.Employee.objects.get(id=pk)
    user=models.User.objects.get(id=employee.user_id)
    user.delete()
    employee.delete()
    return redirect('admin-approve-employee')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_employee_specialisation_view(request):
    employees=models.Employee.objects.all().filter(status=True)
    return render(request,'runsheet/admin_view_employee_specialisation.html',{'employees':employees})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_task_view(request):
    return render(request,'runsheet/admin_task.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_task_view(request):
    tasks=models.Task.objects.all().filter(status=True)
    return render(request,'runsheet/admin_view_task.html',{'tasks':tasks})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_task_from_runsheet_view(request,pk):
    task=models.Task.objects.get(id=pk)
    task.delete()
    return redirect('admin-view-task')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_task_view(request,pk):
    task=models.Task.objects.get(id=pk)

    taskForm=forms.TaskForm(request.FILES,instance=task)
    mydict={'taskForm':taskForm}
    if request.method=='POST':
        taskForm=forms.TaskForm(request.POST,request.FILES,instance=task)
        if taskForm.is_valid():
            task=taskForm.save(commit=False)
            task.status=True
            task.assignedEmployeeId=request.POST.get('assignedEmployeeId')
            task.taskTitle=request.POST.get('taskTitle')
            task.description=request.POST.get('description')
            task.assignDate=request.POST.get('assignDate')
            task.deadlineDate=request.POST.get('deadlineDate')
            task.save()
            return redirect('admin-view-task')
    return render(request,'runsheet/admin_update_task.html',context=mydict)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_task_view(request):
    taskForm=forms.TaskForm()
    mydict={'taskForm':taskForm}
    if request.method=='POST':
        taskForm=forms.TaskForm(request.POST,request.FILES)
        if taskForm.is_valid():

            task=taskForm.save(commit=False)
            task.status=True
            task.assignedEmployeeId=request.POST.get('assignedEmployeeId')
            task.save()

        return HttpResponseRedirect('admin-view-task')
    return render(request,'runsheet/admin_add_task.html',context=mydict)



#------------------FOR APPROVING TASK BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_task_view(request):
    #those whose approval are needed
    tasks=models.Task.objects.all().filter(status=False)
    return render(request,'runsheet/admin_approve_task.html',{'tasks':tasks})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_task_view(request,pk):
    task=models.Task.objects.get(id=pk)
    task.status=True
    task.save()
    return redirect(reverse('admin-approve-task'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_task_view(request,pk):
    task=models.Task.objects.get(id=pk)
    task.delete()
    return redirect('admin-approve-task')



#--------------------- FOR COMPLETING TASK BY ADMIN START-------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_complete_task_view(request):
    tasks=models.Task.objects.all().filter(status=True)
    return render(request,'runsheet/admin_complete_task.html',{'tasks':tasks})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def complete_task_view(request,pk):
    task=models.Task.objects.get(id=pk)
    days=(date.today()-task.assignDate) #2 days, 0:00:00
    assignedEmployee=models.User.objects.all().filter(id=task.assignedEmployeeId)
    d=days.days # only how many day that is 2
    taskDict={
        'taskId':pk,
        'taskTitle':task.taskTitle,
        'description':task.description,
        'assignDate':task.assignDate,
        'deadlineDate':task.deadlineDate,
        'todayDate':date.today(),
        'assignedEmployeeName':assignedEmployee[0].first_name,
    }
    if request.method == 'POST':
        feeDict ={
            'taskTitle':request.POST['taskTitle'],
            'description' : request.POST['description'],
        }
        taskDict.update(feeDict)
        #for updating to database taskCompleteDetails (pDD)
        pDD=models.TaskCompleteDetails()
        pDD.taskId=pk
        pDD.taskTitle=task.taskTitle
        pDD.assignedEmployeeName=assignedEmployee[0].first_name
        pDD.description=task.description
        pDD.comment=task.comment
        pDD.assignDate=date.today()
        pDD.deadlineDate=task.deadlineDate
        pDD.save()
        return render(request,'runsheet/task_final_bill.html',context=taskDict)
    return render(request,'runsheet/task_generate_bill.html',context=taskDict)



#--------------for complete task bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    completeDetails=models.TaskCompleteDetails.objects.all().filter(taskId=pk).order_by('-id')[:1]
    dict={
        'taskTitle':completeDetails[0].taskTitle,
        'assignedEmployeeName':completeDetails[0].assignedEmployeeName,
        'mobile':completeDetails[0].mobile,
        'assignDate':completeDetails[0].assignDate,
        'deadlineDate':completeDetails[0].deadlineDate,
        'description':completeDetails[0].description,
        'comment':completeDetails[0].comment,
        'pdf':completeDetails[0].pdf,
    }
    return render_to_pdf('runsheet/download_bill.html',dict)



#-----------------SCHEDULE START--------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_schedule_view(request):
    return render(request,'runsheet/admin_schedule.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_schedule_view(request):
    schedules=models.Schedule.objects.all().filter(status=True)
    return render(request,'runsheet/admin_view_schedule.html',{'schedules':schedules})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_schedule_view(request):
    scheduleForm=forms.ScheduleForm()
    mydict={'scheduleForm':scheduleForm,}
    if request.method=='POST':
        scheduleForm=forms.ScheduleForm(request.POST)
        if scheduleForm.is_valid():
            schedule=scheduleForm.save(commit=False)
            schedule.taskId=request.POST.get('taskId')
            schedule.employeeId=request.POST.get('employeeId')
            schedule.scheduleStart=request.POST.get('scheduleStart')
            schedule.scheduleFinish=request.POST.get('scheduleFinish')
            schedule.scheduleInfo=request.POST.get('scheduleInfo')
            schedule.employeeName=models.User.objects.get(id=request.POST.get('employeeId')).first_name
            schedule.taskTitle=models.Task.objects.get(id=request.POST.get('taskId')).taskTitle
            schedule.status=True
            schedule.save()
        return HttpResponseRedirect('admin-view-schedule')
    return render(request,'runsheet/admin_add_schedule.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_schedule_view(request):
    #those whose approval are needed
    schedules=models.Schedule.objects.all().filter(status=False)
    return render(request,'runsheet/admin_approve_schedule.html',{'schedules':schedules})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_schedule_view(request,pk):
    schedule=models.Schedule.objects.get(id=pk)
    schedule.status=True
    schedule.save()
    return redirect(reverse('admin-approve-schedule'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_schedule_view(request,pk):
    schedule=models.Schedule.objects.get(id=pk)
    schedule.delete()
    return redirect('admin-approve-schedule')
#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ EMPLOYEE RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='employeelogin')
@user_passes_test(is_employee)
def employee_dashboard_view(request):
    #for three cards
    taskcount=models.Task.objects.all().filter(status=True,assignedEmployeeId=request.user.id).count()
    schedulecount=models.Schedule.objects.all().filter(status=True,employeeId=request.user.id).count()
    taskcompleted=models.TaskCompleteDetails.objects.all().distinct().filter(assignedEmployeeName=request.user.first_name).count()

    #for  table in employee dashboard
    schedules=models.Schedule.objects.all().filter(status=True,employeeId=request.user.id).order_by('-id')
    taskid=[]
    for a in schedules:
        taskid.append(a.taskId)
    tasks=models.Task.objects.all().filter(status=True,assignedEmployeeId__in=taskid).order_by('-id')
    schedules=zip(schedules,tasks)
    mydict={
    'taskcount':taskcount,
    'schedulecount':schedulecount,
    'taskcompleted':taskcompleted,
    'schedules':schedules,
    'employee':models.Employee.objects.get(user_id=request.user.id), #for profile picture of employee in sidebar
    }
    return render(request,'runsheet/employee_dashboard.html',context=mydict)



@login_required(login_url='employeelogin')
@user_passes_test(is_employee)
def employee_task_view(request):
    mydict={
    'employee':models.Employee.objects.get(user_id=request.user.id), #for profile picture of employee in sidebar
    }
    return render(request,'runsheet/employee_task.html',context=mydict)





@login_required(login_url='employeelogin')
@user_passes_test(is_employee)
def employee_view_task_view(request):
    tasks=models.Task.objects.all().filter(status=True,assignedEmployeeId=request.user.id)
    employee=models.Employee.objects.get(user_id=request.user.id) #for profile picture of employee in sidebar
    return render(request,'runsheet/employee_view_task.html',{'tasks':tasks,'employee':employee})


@login_required(login_url='employeelogin')
@user_passes_test(is_employee)
def search_view(request):
    employee=models.Employee.objects.get(user_id=request.user.id) #for profile picture of employee in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    tasks=models.Task.objects.all().filter(status=True,assignedEmployeeId=request.user.id).filter(Q(symptoms__icontains=query)|Q(user__first_name__icontains=query))
    return render(request,'runsheet/employee_view_task.html',{'tasks':tasks,'employee':employee})



@login_required(login_url='employeelogin')
@user_passes_test(is_employee)
def employee_view_complete_task_view(request):
    completedtasks=models.TaskCompleteDetails.objects.all().distinct().filter(assignedEmployeeName=request.user.first_name)
    employee=models.Employee.objects.get(user_id=request.user.id) #for profile picture of employee in sidebar
    return render(request,'runsheet/employee_view_complete_task.html',{'completedtasks':completedtasks,'employee':employee})



@login_required(login_url='employeelogin')
@user_passes_test(is_employee)
def employee_schedule_view(request):
    employee=models.Employee.objects.get(user_id=request.user.id) #for profile picture of employee in sidebar
    return render(request,'runsheet/employee_schedule.html',{'employee':employee})



@login_required(login_url='employeelogin')
@user_passes_test(is_employee)
def employee_view_schedule_view(request):
    employee=models.Employee.objects.get(user_id=request.user.id) #for profile picture of employee in sidebar
    schedules=models.Schedule.objects.all().filter(status=True,employeeId=request.user.id)
    taskid=[]
    for a in schedules:
        taskid.append(a.taskId)
    tasks=models.Task.objects.all().filter(status=True,user_id__in=taskid)
    schedules=zip(schedules,tasks)
    return render(request,'runsheet/employee_view_schedule.html',{'schedules':schedules,'employee':employee})



@login_required(login_url='employeelogin')
@user_passes_test(is_employee)
def employee_delete_schedule_view(request):
    employee=models.Employee.objects.get(user_id=request.user.id) #for profile picture of employee in sidebar
    schedules=models.Schedule.objects.all().filter(status=True,employeeId=request.user.id)
    taskid=[]
    for a in schedules:
        taskid.append(a.taskId)
    tasks=models.Task.objects.all().filter(status=True,user_id__in=taskid)
    schedules=zip(schedules,tasks)
    return render(request,'runsheet/employee_delete_schedule.html',{'schedules':schedules,'employee':employee})



@login_required(login_url='employeelogin')
@user_passes_test(is_employee)
def delete_schedule_view(request,pk):
    schedule=models.Schedule.objects.get(id=pk)
    schedule.delete()
    employee=models.Employee.objects.get(user_id=request.user.id) #for profile picture of employee in sidebar
    schedules=models.Schedule.objects.all().filter(status=True,employeeId=request.user.id)
    taskid=[]
    for a in schedules:
        taskid.append(a.taskId)
    tasks=models.Task.objects.all().filter(status=True,user_id__in=taskid)
    schedules=zip(schedules,tasks)
    return render(request,'runsheet/employee_delete_schedule.html',{'schedules':schedules,'employee':employee})



#---------------------------------------------------------------------------------
#------------------------ EMPLOYEE RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ TASK RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='tasklogin')
@user_passes_test(is_task)
def task_dashboard_view(request):
    task=models.Task.objects.get(user_id=request.user.id)
    employee=models.Employee.objects.get(user_id=task.assignedEmployeeId)
    mydict={
    'task':task,
    'employeeName':employee.get_name,
    'employeeMobile':employee.mobile,
    'employeeAddress':employee.address,
    'symptoms':task.symptoms,
    'employeeDepartment':employee.department,
    'assignDate':task.assignDate,
    }
    return render(request,'runsheet/task_dashboard.html',context=mydict)



@login_required(login_url='tasklogin')
@user_passes_test(is_task)
def task_schedule_view(request):
    task=models.Task.objects.get(user_id=request.user.id) #for profile picture of task in sidebar
    return render(request,'runsheet/task_schedule.html',{'task':task})



@login_required(login_url='tasklogin')
@user_passes_test(is_task)
def task_book_schedule_view(request):
    scheduleForm=forms.TaskScheduleForm()
    task=models.Task.objects.get(user_id=request.user.id) #for profile picture of task in sidebar
    message=None
    mydict={'scheduleForm':scheduleForm,'task':task,'message':message}
    if request.method=='POST':
        scheduleForm=forms.TaskScheduleForm(request.POST)
        if scheduleForm.is_valid():
            print(request.POST.get('employeeId'))
            desc=request.POST.get('description')

            employee=models.Employee.objects.get(user_id=request.POST.get('employeeId'))
            
            schedule=scheduleForm.save(commit=False)
            schedule.employeeId=request.POST.get('employeeId')
            schedule.taskId=request.user.id #----user can choose any task but only their info will be stored
            schedule.employeeName=models.User.objects.get(id=request.POST.get('employeeId')).first_name
            schedule.taskName=request.user.first_name #----user can choose any task but only their info will be stored
            schedule.status=False
            schedule.save()
        return HttpResponseRedirect('task-view-schedule')
    return render(request,'runsheet/task_book_schedule.html',context=mydict)



def task_view_employee_view(request):
    employees=models.Employee.objects.all().filter(status=True)
    task=models.Task.objects.get(user_id=request.user.id) #for profile picture of task in sidebar
    return render(request,'runsheet/task_view_employee.html',{'task':task,'employees':employees})



def search_employee_view(request):
    task=models.Task.objects.get(user_id=request.user.id) #for profile picture of task in sidebar
    
    # whatever user write in search box we get in query
    query = request.GET['query']
    employees=models.Employee.objects.all().filter(status=True).filter(Q(department__icontains=query)| Q(user__first_name__icontains=query))
    return render(request,'runsheet/task_view_employee.html',{'task':task,'employees':employees})




@login_required(login_url='tasklogin')
@user_passes_test(is_task)
def task_view_schedule_view(request):
    task=models.Task.objects.get(user_id=request.user.id) #for profile picture of task in sidebar
    schedules=models.Schedule.objects.all().filter(taskId=request.user.id)
    return render(request,'runsheet/task_view_schedule.html',{'schedules':schedules,'task':task})



@login_required(login_url='tasklogin')
@user_passes_test(is_task)
def task_complete_view(request):
    task=models.Task.objects.get(user_id=request.user.id) #for profile picture of task in sidebar
    completeDetails=models.TaskCompleteDetails.objects.all().filter(taskId=task.id).order_by('-id')[:1]
    taskDict=None
    if completeDetails:
        taskDict ={
        'is_completed':True,
        'task':task,
        'taskId':task.id,
        'taskName':task.get_name,
        'assignedEmployeeName':completeDetails[0].assignedEmployeeName,
        'address':task.address,
        'mobile':task.mobile,
        'symptoms':task.symptoms,
        'assignDate':task.assignDate,
        'releaseDate':completeDetails[0].releaseDate,
        'daySpent':completeDetails[0].daySpent,
        'medicineCost':completeDetails[0].medicineCost,
        'roomCharge':completeDetails[0].roomCharge,
        'employeeFee':completeDetails[0].employeeFee,
        'OtherCharge':completeDetails[0].OtherCharge,
        'total':completeDetails[0].total,
        }
        print(taskDict)
    else:
        taskDict={
            'is_completed':False,
            'task':task,
            'taskId':request.user.id,
        }
    return render(request,'runsheet/task_complete.html',context=taskDict)


#------------------------ TASK RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------








#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'runsheet/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'runsheet/contactussuccess.html')
    return render(request, 'runsheet/contactus.html', {'form':sub})


#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------

