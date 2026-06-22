from django.contrib import admin
from .models import Company, Student, Placement

# This code creates the search bars, filters, and tables in the UI
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'company_name', 'tier')
    search_fields = ('company_name',)
    list_filter = ('tier',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'name', 'specialization', 'cgpa', 'is_placed')
    search_fields = ('roll_no', 'name')
    list_filter = ('specialization', 'is_placed')

@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ('placement_id', 'student', 'company', 'package_lpa')
    search_fields = ('student__roll_no', 'student__name', 'company__company_name')
    list_filter = ('company__tier',)
