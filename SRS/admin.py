from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(university)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(course)
admin.site.register(Attendance)
admin.site.register(SRS)
admin.site.register(SRS_Question)