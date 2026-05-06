from django.contrib import admin
from .models import Class, Assignment, Submission, AssignmentFile, Membership
# Register your models here.
admin.site.register(Class)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(AssignmentFile)
admin.site.register(Membership)