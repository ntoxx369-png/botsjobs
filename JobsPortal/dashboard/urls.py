from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('jobs/', views.manage_jobs, name='manage_jobs'),
    path('jobs/create/', views.create_job, name='create_job'),
    path('jobs/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('jobs/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('jobs/<int:job_id>/applications/', views.view_applications, name='view_applications'),
    path('gigs/', views.manage_gigs, name='manage_gigs'),
    path('gigs/create/', views.create_gig, name='create_gig'),
    path('gigs/<int:gig_id>/edit/', views.edit_gig, name='edit_gig'),
    path('gigs/<int:gig_id>/delete/', views.delete_gig, name='delete_gig'),
    path('gigs/<int:gig_id>/applications/', views.view_gig_applications, name='view_gig_applications'),
    path('featured/', views.featured_jobs, name='featured_jobs'),
    path('featured/<int:job_id>/upgrade/', views.upgrade_job, name='upgrade_job'),
    path('company/edit/', views.edit_company_profile, name='edit_company_profile'),
]