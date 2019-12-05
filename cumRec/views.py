from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
#from django.db.models import Q
from django.urls import reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout

#from .forms import UserSignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
#import simplejson
from .models import Student, StudentRecord
from .forms import (
	#UserForm, 
    UserSignUpForm,
	StudentCreateForm, 
	StudentUpdateForm, 
	StudentRecordsCreateForm, 
	StudentRecordsUpdateForm
	)


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

# Create your views here.

'''
class HomeView(LoginRequiredMixin, ListView):
    template_name = 'home.html'
    context_object_name = 'students'

    def get_queryset(self):
        return Student.objects.all()
'''


class StudentListView(LoginRequiredMixin, ListView):
	template_name = 'cumRec/student_list.html'
	context_object_name = 'students'

	def get_queryset(self):
		return Student.objects.all()


'''
class StudentCreateView(LoginRequiredMixin, CreateView):
	template_name = 'cumRec/student_form.html'
	form_class = StudentCreateForm
'''

#@login_required(login_url='/login/')
def create_student(request):
    if not request.user.is_authenticated:
        return render(request, 'cumRec/login.html')
    else:
        form = StudentCreateForm(request.POST or None, request.FILES or None)
        #student = get_object_or_404(Student, pk=pk)
        student = Student.objects.all()
        if form.is_valid():
        	
	        for s in student:
                    
	            if s.studentID == form.cleaned_data.get("studentID"):
	                context = {
	                    'student': student,
	                    'form': form,
	                    'error_message': 'You already added that student',
	                }
	                return render(request, 'cumRec/student_form.html', context)
	        student = form.save(commit=False)

	        student.user = request.user
	        student.photo = request.FILES['photo']
	        file_type = student.photo.url.split('.')[-1]
	        file_type = file_type.lower()
	        if file_type not in IMAGE_FILE_TYPES:
	            context = {
	                'student': student,
	                'form': form,
	                'error_message': 'Image file must be PNG, JPG, or JPEG',
	            }
	            return render(request, 'cumRec/student_form.html', context)
	        student.save()
	        return render(request, 'cumRec/student_list.html', {'student': student})
        context = {
            "form": form,
        }
        return render(request, 'cumRec/student_form.html', context)


'''
class StudentDetailView(LoginRequiredMixin, DetailView):
	model = Student
	template_name = 'cumRec/student_detail.html'

	#def get_queryset(self):
	#	return Student.objects.all()
'''
def student_detail_view(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'cumRec/login.html')
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        raise Http404("Student does not exist")
    context = {
        "student": student,
        "studentrecords": student.studentrec.all(),
        #"nonRecordStudents": student.objects.exclude(studentrecords=studentrecords).all(),
        #for students without records
    }
    return render(request, "cumRec/student_detail.html", context)


class StudentUpdateView(LoginRequiredMixin, UpdateView):
	template_name = 'cumRec/student_form.html'
	form_class = StudentUpdateForm
	success_url = reverse_lazy('cumRec:studentList')

	def get_queryset(self):
		return Student.objects.all()


class StudentDeleteView(LoginRequiredMixin, DeleteView):
	model = Student
	success_url = reverse_lazy('cumRec:studentList')


#student records
'''
class StudentRecordsListView(LoginRequiredMixin, ListView):
	template_name = 'cumRec/student_records_list.html'
	context_object_name = 'studentrecords'
	success_url = reverse_lazy('cumRec:studentRecordsDetail')

	def get_queryset(self):
		return StudentRecord.objects.all()
'''

'''
class StudentRecordsCreateView(LoginRequiredMixin, CreateView):
	template_name = 'cumRec/student_records_form.html'
	form_class = StudentRecordsCreateForm

	def get_queryset(self):
		return StudentRecord.objects.all()	
'''

def create_student_record(request):
    if not request.user.is_authenticated:
        return render(request, 'cumRec/login.html')
    else:
        form = StudentRecordsCreateForm(request.POST or None, request.FILES or None)
        studentrec = StudentRecord.objects.all()
        if form.is_valid():
            
            for r in studentrec:
                if r.subject == form.cleaned_data.get("subject"):
                    context = {
                        'studentrec': studentrec,
                        'form': form,
                        'error_message': 'You already added that subject',
                    }
                    return render(request, 'cumRec/student_records_form.html', context)
            studentrec = form.save(commit=False)

            studentrec.user = request.user

            studentrec.save()
            return render(request, 'cumRec/student_records_detail.html', {'studentrec': studentrec})
        context = {
            "form": form,
        }
        return render(request, 'cumRec/student_records_form.html', context)


'''
class StudentRecordsDetailView(LoginRequiredMixin, DetailView):
	model = StudentRecord
	template_name = 'cumRec/student_records_detail.html'
	success_url = reverse_lazy('cumRec:studentRecordsList')

	def get_queryset(self):
		return StudentRecord.objects.all()
'''
def student_records_detail_view(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'cumRec/login.html')
    try:
        student = Student.objects.get(pk=pk)
        studentwithrecord = StudentRecord.objects.get(pk=pk)
    except Student.DoesNotExist:
        raise Http404("Student does not exist")
    context = {
        "student": student,
        "studentrecords": student.studentrec.all(),
        #"nonRecordStudents": Student.objects.exclude(pk=pk).all()
        #for students without records
    }
    return render(request, "cumRec/student_records_detail.html", context)


class StudentRecordsUpdateView(LoginRequiredMixin, UpdateView):
	template_name = 'cumRec/student_records_form.html'
	form_class = StudentRecordsUpdateForm
	success_url = reverse_lazy('cumRec:studentList')

	def get_queryset(self):
		return StudentRecord.objects.all()


#for dependent/chained select
def load_subject(request):
    course_id = request.GET.get('course')
    subjects = Subject.objects.filter(course_id=course_id).order_by('course')
    return render(request, 'cumRec/student_subject_options.html', {'subjects': subjects})


''' for authentication and login
---------------------------------------------------------- '''

def logout_user(request):
    logout(request)
    return render(request, "cumRec/accounts/logout.html", {"message": "Logged out."})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                student = Student.objects.filter(user=request.user)
                return render(request, 'cumRec/student_list.html', {'student': student})
            else:
                return render(request, 'cumRec/accounts/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'cumRec/accounts/login.html', {'error_message': 'Invalid login'})
    return render(request, 'cumRec/accounts/login.html')



def usersignup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('cumRec/accounts/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                #'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
    else:
        form = UserSignUpForm()
    return render(request, 'cumRec/accounts/registration_form.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activate successfully')
    else:
        return HttpResponse('Activation link is invalid!')









'''
class UserFormView(View):
	form_class = UserForm
	template_name = 'cumRec/accounts/registration_form.html'

	#display blank form
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	#process form data
	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():

			user = form.save(commit=False)

			#cleaned (normalised) data
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			#changing password
			user.set_password(password)
			user.save()

			#returns users object if credentials are correct
			user = authenticate(username=username, password=password)

			if user is not None:

				if user.is_active:
					login(request, user)
					return redirect('cumRec:loginUser')

		return render(request, self.template_name, {'form': form})'''

''' End authentication and login
---------------------------------------------------------- '''



def search(request):
        student = Student.objects.filter(user=request.user)
        studentrecords = StudentRecord.objects.all()
        query = request.GET.get("q")
        if query:
            student = student.filter(
                Q(studentID__icontains=query) |
                Q(firstName__icontains=query)
            ).distinct()
            studentrecords = studentrecords.filter(
                Q(subject__icontains=query)
            ).distinct()
            return render(request, 'cumRec/studentList.html', {
                'student': student,
                'studentrecords': studentrecords,
            })
        else:
            return render(request, 'cumRec/studentList.html', {'student': student})

