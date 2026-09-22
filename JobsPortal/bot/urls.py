from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from jobs.models import Employer, Gig, Job


def home(request):
    featured_jobs = Job.objects.filter(is_active=True).order_by('-is_featured', '-created_at')[:6]
    featured_gigs = Gig.objects.filter(status='open').order_by('-is_featured', '-created_at')[:3]
    locations = Job._meta.get_field('location').choices
    stats = {
        'jobs_count': Job.objects.filter(is_active=True).count(),
        'gigs_count': Gig.objects.filter(status='open').count(),
        'employers_count': Employer.objects.count(),
    }
    return render(request, 'home.html', {
        'featured_jobs': featured_jobs,
        'featured_gigs': featured_gigs,
        'locations': locations,
        'stats': stats,
    })


def post_job(request):
    locations = Job._meta.get_field('location').choices
    stats = {
        'jobs_count': Job.objects.filter(is_active=True).count(),
        'gigs_count': Gig.objects.filter(status='open').count(),
        'employers_count': Employer.objects.count(),
    }
    return render(request, 'post_job.html', {'locations': locations, 'stats': stats})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('post-job/', post_job, name='post_job'),
    path('jobs/', include('jobs.urls')),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)