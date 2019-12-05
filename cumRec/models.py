from django.contrib.auth.models import Permission, User
from django.db import models
from django.urls import reverse


# Create your models here.

class School(models.Model):
	schoolName = models.CharField(max_length=64)

	def __str__(self):
		return f'{self.schoolName}'


class Course(models.Model):
	courseName = models.CharField(max_length=64)
	courseCategory = models.CharField(max_length=10)

	def __str__(self):
		return f'{self.courseName}'


class Subject(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='subjectcourse')
	subjectName = models.CharField(max_length=64)
	subjectCategory = models.CharField(max_length=10)

	def __str__(self):
		return f'{self.subjectName}'


class Examiner(models.Model):
	examinerName = models.CharField(max_length=64)

	def __str__(self):
		return f'{self.examinerName}'


class ExaminerGrade(models.Model):
	gradeName = models.CharField(max_length=64)

	def __str__(self):
		return f'{self.gradeName}'


class Student(models.Model):
	user = models.ForeignKey(User, default=1, on_delete=models.CASCADE, related_name="user")
	photo = models.FileField()
	school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="studentschoool")
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='studentcourse')
	studentID = models.CharField(max_length=25)
	firstName = models.CharField(max_length=64)
	lastName = models.CharField(max_length=64)
	otherNames = models.CharField(max_length=64, null=True, blank=True)
	birthDate = models.DateField(auto_now=False, auto_now_add=False)
	gender = models.CharField(max_length=25)
	region = models.CharField(max_length=64, null=True, blank=True)
	nationality = models.CharField(max_length=64)
	email = models.EmailField(max_length=64, null=True, blank=True)
	mobile = models.IntegerField(null=True, blank=True)
	indexNumber = models.CharField(max_length=25, null=True, blank=True)
	admissionYear = models.DateField(max_length=64, auto_now_add=False)
	completionYear = models.DateField(max_length=64, auto_now_add=False, null=True, blank=True)
	completed = models.BooleanField(null=True, blank=True)
	timeSubmitted = models.DateTimeField(auto_now_add=True)
	updatedTime = models.DateTimeField(auto_now=True)
	beceResult = models.FileField(null=True, blank=True)

	# Reverse to studentdetail page using self.pk
	def get_absolute_url(self):
		return reverse('cumRec:studentDetail', kwargs={'pk': self.pk})

	def __str__(self):
		return f'{self.studentID}'

	class Meta:
		ordering = ['-updatedTime', '-timeSubmitted']#updated last shows first


class StudentRecord(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="studentrec")
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="courserec")
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="subjectrec")
	form1Term1 = models.IntegerField(null=True, blank=True)
	form1Term2 = models.IntegerField(null=True, blank=True)
	form1Term3 = models.IntegerField(null=True, blank=True)
	form2Term1 = models.IntegerField(null=True, blank=True)
	form2Term2 = models.IntegerField(null=True, blank=True)
	form2Term3 = models.IntegerField(null=True, blank=True)
	form3Term1 = models.IntegerField(null=True, blank=True)
	form3Term2 = models.IntegerField(null=True, blank=True)
	form3Term3 = models.IntegerField(null=True, blank=True)
	capstoneExam = models.IntegerField(null=True, blank=True)
	totalScore = models.IntegerField(null=True, blank=True)
	averageScore = models.IntegerField(null=True, blank=True)
	gpa = models.IntegerField(null=True, blank=True)
	examinerName = models.ForeignKey(Examiner, null=True, on_delete=models.CASCADE, blank=True, related_name="examinerrec")
	gradeName = models.ForeignKey(ExaminerGrade, null=True, on_delete=models.CASCADE, blank=True, related_name="graderec")
	finalResult = models.FileField(null=True, blank=True)
	timeSubmitted = models.DateTimeField(auto_now_add=True)
	updatedTime = models.DateTimeField(auto_now=True)

	# Reverse to studentDetail page using self.pk
	def get_absolute_url(self):
		return reverse('cumRec:studentRecordsDetail', kwargs={'pk': self.pk})

	def __str__(self):
		return f'{self.student} {self.subject}'
	
	class Meta:
		ordering = ['-updatedTime', '-timeSubmitted']#updated last shows first

