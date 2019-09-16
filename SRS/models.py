from __future__ import unicode_literals

from django.db import models

# Create your models here.

class university(models.Model):
	uniName = models.CharField(max_length = 200)
	uniCode = models.AutoField(primary_key = True)

	def __str__(self):
		return self.uniName

class Student(models.Model):
	uniCode = models.IntegerField()
	studentName = models.CharField(max_length = 50)
	studentCode = models.AutoField(primary_key = True)
	batch = models.CharField(max_length = 5)
	mail = models.CharField(null = True, max_length = 150)
	passkey = models.CharField(max_length = 160)

	def __str__(self):
		return self.studentName

class Faculty(models.Model):
	uniCode = models.IntegerField()
	facultyName = models.CharField(max_length = 50)
	facultyCode = models.AutoField(primary_key = True)
	passkey = models.CharField(max_length = 160)

	def __str__(self):
		return self.facultyName

class course(models.Model):
	courseCode = models.CharField(max_length = 6, primary_key = True)
	courseName = models.CharField(max_length = 50)
	attendance_criteria = models.IntegerField()

	def __str__(self):
		return self.courseCode

class Attendance(models.Model):
	studentID = models.IntegerField()
	facultyID = models.IntegerField()
	courseCode = models.CharField(max_length = 6)
	attended = models.IntegerField()
	bunked = models.IntegerField()

	def __str__(self):
		return str(self.studentID) + "_" + str(self.facultyID) + "_" + self.courseCode

class SRS(models.Model):
	studentID = models.IntegerField()
	facultyID = models.IntegerField()
	feedback = models.TextField()
	links = models.TextField()
	feedbackScore = models.FloatField()

	def __str__(self):
		return str(self.studentID) + "_" + str(self.facultyID)

class SRS_Question(models.Model):
	quesCode = models.CharField(max_length = 5, primary_key = True)
	quesText = models.TextField()

	def __str__(self):
		return self.quesCode