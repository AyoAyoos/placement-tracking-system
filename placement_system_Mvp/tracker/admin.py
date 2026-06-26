from django.contrib import admin
from .models import Company, Student, Placement, Internship

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'domain')
    search_fields = ('name', 'domain')
    list_filter = ('city',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('enrollment_no', 'full_name', 'class_division', 'batch', 'department')
    search_fields = ('enrollment_no', 'roll_no', 'full_name', 'email')
    list_filter = ('batch', 'class_division', 'department')

@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ('student', 'company', 'ctc_lpa', 'role', 'month_of_offer')
    search_fields = ('student__full_name', 'student__enrollment_no', 'company__name')
    list_filter = ('company__name', 'month_of_offer')

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ('student', 'company', 'duration_months', 'mode', 'stipend_monthly', 'source')
    search_fields = ('student__full_name', 'student__enrollment_no', 'company__name')
    list_filter = ('mode', 'source', 'company__name')
