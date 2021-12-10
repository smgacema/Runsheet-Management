from django.contrib import admin
from .models import Employee,Task,Schedule,TaskCompleteDetails

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Employee, EmployeeAdmin)

class TaskAdmin(admin.ModelAdmin):
    pass
admin.site.register(Task, TaskAdmin)

class ScheduleAdmin(admin.ModelAdmin):
    pass
admin.site.register(Schedule, ScheduleAdmin)

class TaskCompleteDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(TaskCompleteDetails, TaskCompleteDetailsAdmin)