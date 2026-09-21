from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('jobs/', views.manage_jobs, name='manage_jobs'),
    path('jobs/create/', views.create_job, name='create_job'),
    path('jobs/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('jobs/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('jobs/<int:job_id>/applications/', views.view_applications, name='view_applications'),
    path('company/edit/', views.edit_company_profile, name='edit_company_profile'),
]