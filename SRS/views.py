from django.shortcuts import render
from SRS.models import *
import hashlib
from matplotlib import pyplot as plt

def getEncryption(key):
	return hashlib.sha256(key).hexdigest()

def student_login(request, userID, password, uniCode):
	userData = Student.objects.all()
	for user in userData:
		if user.studentCode == userID:
			if user.passkey == password and user.uniCode == uniCode:
				attendanceObjects = Attendance.objects.filter(studentID = userID)
				qualified = []
				faculty = []
				subjects = []
				facultyData = {'facultyID': 0, 'facultyName': ''}
				for att in attendanceObjects:
					facultyData['facultyID'] = att.facultyID
					facultyData['facultyName'] = Faculty.objects.get(facultyCode = att.facultyID)
					faculty.append(facultyData)
					criteria = course.objects.get(courseCode = att.courseCode).attendance_criteria
					subjects.append(course.objects.get(courseCode = att.courseCode))
					if float(att.attended) + float(att.bunked) == 0:
						qualified.append(True)
					elif float(att.attended)/(float(att.attended) + float(att.bunked)) >= float(criteria) / 100:
						qualified.append(True)
					else:
						qualified.append(False)
				return render(request, 'SRS/dashboard_students.html',
					{'student': user,
					'uni': university.objects.filter(uniCode = user.uniCode)[0],
					'Attendance': zip(attendanceObjects, qualified),
					'faculty_tagged': faculty,
					'subjects': subjects})
			else:
				return render(request, 'SRS/errPage.html', {'message': 'Invalid Credentials'})
	return render(request, 'SRS/errPage.html', {'message': 'Invalid Credentials'})

def faculty_login(request, userID, password, uniCode):
	userData = Faculty.objects.all()
	for user in userData:
		if user.facultyCode == userID:
			if user.passkey == password and user.uniCode == uniCode:
				attendanceDetails = Attendance.objects.filter(facultyID = user.facultyCode).order_by('courseCode')
				batchList = Student.objects.values('batch').distinct()
				students = []
				return render(request, 'SRS/dashboard_faculty.html', {
					'user': user, 'uni': university.objects.filter(uniCode = user.uniCode)[0],
					'attendance': attendanceDetails,
					'batches': batchList
					})
			else:
				return render(request, 'SRS/errPage.html', {'message': 'Invalid Credentials'})
	return render(request, 'SRS/errPage.html', {'message': 'Invalid Credentials'})

# Create your views here.

def index(request):
	univList = university.objects.order_by('uniName')
	return render(request, 'SRS/index.html', {'univs': univList})

def login(request):
	if request.method != "POST":
		return render(request, 'SRS/errPage.html', {'message': 'Unauthorized Request for Login'})
	uniCode = int(request.POST['uniName'])
	userID = int(request.POST['user_id'])
	password = getEncryption(request.POST['passkey'])
	access = request.POST['access']
	if access == 'S':
		return student_login(request, userID, password, uniCode)
	elif access == 'F':
		return faculty_login(request, userID, password, uniCode)

def updateAttendance(request):
	if request.method != "POST":
		return render(request, 'SRS/errPage.html', {'message': 'Unauthorized Request for Update'})
	facultyCode = request.POST['fCode']
	attendanceDetails = Attendance.objects.filter(facultyID = facultyCode).order_by('courseCode')
	for attendance in attendanceDetails:
		attendance.attended = (request.POST[(attendance.courseCode + '_' + str(attendance.studentID) + '_Att').encode('ascii', 'ignore')])
		attendance.bunked = (request.POST[attendance.courseCode + '_' + str(attendance.studentID) + '_Bun'])
		attendance.save()
	user = Faculty.objects.get(facultyCode = facultyCode)
	batchList = Student.objects.values('batch').distinct()
	return render(request, 'SRS/dashboard_faculty.html', {
		'user': user,
		'uni': university.objects.filter(uniCode = user.uniCode)[0],
		'attendance': attendanceDetails,
		'batches': batchList
		})

def uPwd_stud(request):
	if request.method != "POST":
		return render(request, 'SRS/errPage.html', {'message': 'Unauthorized Request for Update'})
	p = request.POST['psd']
	if p != request.POST['psdc']:
		return render(request, 'SRS/errPage.html', {'message': 'Passwords Do Not Match'})
	p = getEncryption(p)
	user = Student.objects.get(studentCode = request.POST['sCode'])
	user.passkey = p
	user.save()
	attendanceObjects = Attendance.objects.filter(studentID = request.POST['sCode'])
	qualified = []
	for att in attendanceObjects:
		criteria = course.objects.get(courseCode = att.courseCode).attendance_criteria
		if float(att.attended) + float(att.bunked) == 0:
			qualified.append(True)
		elif float(att.attended)/(float(att.attended) + float(att.bunked)) >= float(criteria) / 100:
			qualified.append(True)
		else:
			qualified.append(False)
	return render(request, 'SRS/dashboard_students.html',
		{'student': user, 'uni': university.objects.filter(uniCode = user.uniCode)[0],
		'Attendance': zip(attendanceObjects, qualified)})

def uPwd_fac(request):
	if request.method != "POST":
		return render(request, 'SRS/errPage.html', {'message': 'Unauthorized Request for Update'})
	p = request.POST['psd']
	if p != request.POST['psdc']:
		return render(request, 'SRS/errPage.html', {'message': 'Passwords Do Not Match'})
	p = getEncryption(p)
	user = Faculty.objects.get(facultyCode = request.POST['fCode'])
	user.passkey = p
	user.save()
	attendanceDetails = Attendance.objects.filter(facultyID = user.facultyCode).order_by('courseCode')
	return render(request, 'SRS/dashboard_faculty.html', {
		'user': user, 'uni': university.objects.filter(uniCode = user.uniCode)[0],
		'attendance': attendanceDetails
		})

def loadSRS(request):
	if request.method != "POST":
		return render(request, 'SRS/errPage.html', {'message': 'Unauthorized Request for Module'})
	studentID = request.POST['sCode']
	facultyID = request.POST['fCode']
	facultyName = Faculty.objects.get(facultyCode = facultyID)
	studentName = Student.objects.get(studentCode = studentID)
	ques = SRS_Question.objects.all()
	return render(request, 'SRS/SRS_Module.html', {
		'fName': facultyName,
		'sName': studentName,
		'fCode': facultyID,
		'sCode': studentID,
		'question': ques
		})

def submitSRS(request):
	if request.method != "POST":
		return render(request, 'SRS/errPage.html', {'message': 'Unauthorized Request for SRS Submission'})
	fCode = request.POST['f']
	sCode = request.POST['s']
	# return render(request, 'SRS/errPage.html', {'message': [Student.objects.get(studentCode = sCode).passkey,Student.objects.get(studentCode = sCode).uniCode]})
	fbk = request.POST['feedback']
	link_count = request.POST['lCount']
	links = []
	for i in range(int(link_count)):
		links.append(request.POST['link_' + str(i)])
	links = ','.join(links)
	from nltk.sentiment import SentimentIntensityAnalyzer
	fbs = SentimentIntensityAnalyzer().polarity_scores(fbk)['compound']
	data = SRS(studentID = sCode, facultyID = fCode, feedback = fbk, links = links, feedbackScore = fbs)
	data.save()
	return student_login(
		request,
		int(sCode),
		str(Student.objects.get(studentCode = sCode).passkey),
		int(Student.objects.get(studentCode = sCode).uniCode)
		)

def update_by_list(request):
	if request.method != "POST":
		return render(request, 'SRS/errPage.html', {'message': 'Unauthorized Request for Update'})
	studentList = request.POST['studentsList'].replace('\r', '').split('\n')
	batch = request.POST['batch']
	all_students = [student[0] for student in Student.objects.filter(batch = batch).values_list('studentCode')]
	for student in all_students:
		if str(student) in studentList:
			# present
			stud_det = Attendance.objects.get(studentID = str(student), facultyID = request.POST['fCode'])
			stud_det.attended = int(stud_det.attended) + 1
			stud_det.save()
		else:
			# absent
			stud_det = Attendance.objects.get(studentID = str(student), facultyID = request.POST['fCode'])
			stud_det.bunked = int(stud_det.bunked) + 1
			stud_det.save()
	user = Faculty.objects.get(facultyCode = request.POST['fCode'])
	batchList = Student.objects.values('batch').distinct()
	return render(request, 'SRS/dashboard_faculty.html', {
		'user': user,
		'uni': university.objects.filter(uniCode = user.uniCode)[0],
		'attendance': Attendance.objects.filter(facultyID = request.POST['fCode']).order_by('courseCode'),
		'batches': batchList
		})

def getGraphs(request):
	if request.method != "POST":
		return render(request, 'SRS/errPage.html', {'message': 'Unauthorized Request for Access'})
	pie_values = [0, 0]
	fID = request.POST['fCode']
	ratings = SRS.objects.filter(facultyID = fID)
	return render(request, 'SRS/graphs.html', {'fCode': fID})

def goBack(request):
	fCode = request.POST['fCode']
	return faculty_login(
		request,
		int(fCode),
		str(Faculty.objects.get(facultyCode = fCode).passkey),
		int(Faculty.objects.get(facultyCode = fCode).uniCode)
		)