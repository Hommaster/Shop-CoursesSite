from django.contrib import admin
from .models import PaymentCourses


@admin.register(PaymentCourses)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['coursep', 'profilep', 'price', 'paid']
