from django.contrib import admin
from .models import PayCourse


@admin.register(PayCourse)
class PayCourseAdmin(admin.ModelAdmin):
    list_display = ['course', 'price']
