from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from cumRec.models import Student, StudentRecord, Subject



class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required')
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


'''
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
'''

class StudentCreateForm(forms.ModelForm):
	
	class Meta:
		model = Student
		fields = '__all__'
'''		fields = [
		'photo', 'school', 'course', 'studentID', 'firstName', 'lastName', 'otherNames', 'birthDate', 
		'gender', 'region', 'nationality', 'email', 'mobile', 'indexNumber', 'admissionYear', 'completionYear', 
		'completed'
		]'''


class StudentUpdateForm(forms.ModelForm):
	
	class Meta:
		model = Student
		fields = [
		'photo', 'school', 'course', 'studentID', 'firstName', 'lastName', 'otherNames', 'birthDate', 
		'gender', 'region', 'nationality', 'email', 'mobile', 'indexNumber', 'admissionYear', 'completionYear', 
		'completed'
		]


class StudentRecordsCreateForm(forms.ModelForm):

	class Meta:
		model = StudentRecord
		#fields = '__all__'
		fields = [
		'student', 'course', 'subject', 'form1Term1', 'form1Term2', 'form1Term3', 'form2Term1', 'form2Term2',
		'form2Term3', 'form3Term1', 'form3Term2', 'form3Term3', 'capstoneExam', 'totalScore', 'averageScore',
		'gpa', 'examinerName', 'gradeName'
		]

	#for dependent/chained select		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['subject'].queryset = Subject.objects.none()

		if 'course' in self.data:
			try:
				course_id = int(self.data.get('course'))
				self.fields['subject'].queryset = Subject.objects.filter(course_id=course_id).order_by('course')
			except (ValueError, TypeError):
				pass  # invalid input from the client; ignore and fallback to empty subject queryset
		elif self.instance.pk:
			self.fields['subject'].queryset = self.instance.course.subject_set.order_by('course')


class StudentRecordsUpdateForm(forms.ModelForm):
	
	class Meta:
		model = StudentRecord
		fields = [
		'student', 'course', 'subject', 'form1Term1', 'form1Term2', 'form1Term3', 'form2Term1', 'form2Term2',
		'form2Term3', 'form3Term1', 'form3Term2', 'form3Term3', 'capstoneExam', 'totalScore', 'averageScore',
		'gpa', 'examinerName', 'gradeName'
		]
