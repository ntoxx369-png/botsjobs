from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Job, Employer, Applicant


def job_list(request):
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')

    query = request.GET.get('q')
    location = request.GET.get('location')
    job_type = request.GET.get('job_type')
    industry = request.GET.get('industry')

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(employer__company_name__icontains=query)
        )

    if location:
        jobs = jobs.filter(location=location)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    if industry:
        jobs = jobs.filter(industry=industry)

    paginator = Paginator(jobs, 20)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)

    locations = Job._meta.get_field('location').choices
    job_types = Job._meta.get_field('job_type').choices
    industries = Job._meta.get_field('industry').choices

    context = {
        'jobs': jobs,
        'locations': locations,
        'job_types': job_types,
        'industries': industries,
    }
    return render(request, 'jobs/job_list.html', context)


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)
    job.views += 1
    job.save()
    related_jobs = Job.objects.filter(
        Q(industry=job.industry) | Q(location=job.location),
        is_active=True
    ).exclude(id=job.id)[:4]

    context = {
        'job': job,
        'related_jobs': related_jobs,
    }
    return render(request, 'jobs/job_detail.html', context)


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        cover_letter = request.POST.get('cover_letter', '')
        resume = request.FILES.get('resume')

        applicant = Applicant.objects.create(
            job=job,
            full_name=full_name,
            email=email,
            phone=phone,
            cover_letter=cover_letter,
            resume=resume
        )

        send_mail(
            subject=f'Application Received: {job.title}',
            message=f'Dear {full_name},\n\nWe have received your application for {job.title} at {job.employer.company_name}. We will review your application and get back to you soon.\n\nBest regards,\n{job.employer.company_name}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )

        send_mail(
            subject=f'New Application: {applicant.full_name} for {job.title}',
            message=f'A new application has been received.\n\nName: {applicant.full_name}\nEmail: {applicant.email}\nPhone: {applicant.phone}\n\nLogin to the admin panel to view the full application.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=True,
        )

        return render(request, 'jobs/application_success.html', {'job': job})

    context = {'job': job}
    return render(request, 'jobs/apply.html', context)