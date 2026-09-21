from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employer, Job, Applicant, Resume


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'industry', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'industry']
    search_fields = ['company_name', 'industry']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'location', 'job_type', 'is_active', 'deadline', 'created_at']
    list_filter = ['job_type', 'industry', 'location', 'is_active']
    search_fields = ['title', 'description', 'employer__company_name']
    raw_id_fields = ['employer']


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'job', 'applied_at']
    list_filter = ['applied_at']
    search_fields = ['full_name', 'email', 'job__title']


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'headline', 'updated_at']
    search_fields = ['full_name', 'user__username']