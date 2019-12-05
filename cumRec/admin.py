from django.contrib import admin
from .models import Student, Course, Subject, School, Examiner, StudentRecord, ExaminerGrade



# Register your models here.

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(School)
admin.site.register(Examiner)
admin.site.register(ExaminerGrade)
admin.site.register(StudentRecord)