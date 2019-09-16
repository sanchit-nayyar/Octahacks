from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='SRS'),
	url(r'^login/$', views.login, name='login'),
	url(r'^updateAttendance/$', views.updateAttendance, name='Update Attendance'),
	url(r'^update_password_student/$', views.uPwd_stud, name='Update Student Password'),
	url(r'^update_password_faculty/$', views.uPwd_fac, name='Update Faculty Password'),
	url(r'^loadSRS/$', views.loadSRS, name='Load SRS Module'),
	url(r'^upload_SRS/$', views.submitSRS, name='Submit Student Feedback'),
	url(r'^update_by_list/$', views.update_by_list, name='Update Attendance by List'),
	url(r'^getGraph/$', views.getGraphs, name='Get Graphs'),
	url(r'^goBack/$', views.goBack, name = 'SRS Module Faculty')
]