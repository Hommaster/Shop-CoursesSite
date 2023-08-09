from django.contrib import admin

from .models import Subject, Course, Module


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title', )}


class ModuleInline(admin.TabularInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'owner', 'created', 'updated']
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ['title', 'owner']
    list_filter = ['created', 'subject']
    inlines = [ModuleInline]
