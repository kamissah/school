from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'cumRec'

urlpatterns = [

	#path('createaccount/', views.UserFormView.as_view(), name='register'),
	#path('activate/<slug:uidb64>/<slug:token>/', views.activate_account, name='activate'), + other update: urlsafe_base64_encode(force_bytes(user.pk)).decode(), ==> urlsafe_base64_encode(force_bytes(user.pk)
	
	path('createaccount/', views.usersignup, name='register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_account, name='activate'),
	path('login/', views.login_user, name='loginUser'),
	path('', views.StudentListView.as_view(), name='studentList'),
	path('logout', views.logout_user, name='logoutUser'),	
	#cumRec/student/create/
	#path('student/create/', views.StudentCreateView.as_view(), name='studentCreate'),
	path('student/create/', views.create_student, name='studentCreate'),
	#cumRec/student/1/detail/
	#path('student/<int:pk>/detail/', views.StudentDetailView.as_view(), name='studentDetail'),
	path('student_<int:pk>/detail/', views.student_detail_view, name='studentDetail'),
	path('student_<int:pk>/update/', views.StudentUpdateView.as_view(), name='studentUpdate'),
	#cumRec/student/pk/delete/
	path('student_<int:pk>/delete/', views.StudentDeleteView.as_view(), name='studentDelete'),
	
	#cumRec/studentrecords/create/
	#path('studentrec/create/', views.StudentRecordsCreateView.as_view(), name='studentRecordsCreate'),
	path('studentrec/create/', views.create_student_record, name='studentRecordsCreate'),
	#path('studentrec/list/', views.StudentRecordsListView.as_view(), name='studentRecordsList'),
	#path('studentrec/<int:pk>/detail/', views.StudentRecordsDetailView.as_view(), name='studentRecordsDetail'),
	path('student_<int:pk>_rec/detail/', views.student_records_detail_view, name='studentRecordsDetail'),
	path('student_<int:pk>_rec/update/', views.StudentRecordsUpdateView.as_view(), name='studentRecordsUpdate'),

	path('ajax/loadsubject/', views.load_subject, name='ajaxLoadSubject'),	
	path('search/', views.search, name='search')

]