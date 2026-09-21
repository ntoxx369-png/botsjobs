from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from jobs.models import Job, Employer, Applicant
from django.db.models import Sum
from django.utils import timezone


@login_required
def dashboard_home(request):
    try:
        employer = request.user.employer_profile
    except Employer.DoesNotExist:
        messages.error(request, 'You are not registered as an employer.')
        return redirect('home')

    jobs = Job.objects.filter(employer=employer).order_by('-created_at')
    total_jobs = jobs.count()
    active_jobs = jobs.filter(is_active=True).count()
    total_views = jobs.aggregate(total=Sum('views'))['total'] or 0
    total_applications = Applicant.objects.filter(job__employer=employer).count()

    recent_applications = Applicant.objects.filter(
        job__employer=employer
    ).select_related('job').order_by('-applied_at')[:10]

    context = {
        'employer': employer,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_views': total_views,
        'total_applications': total_applications,
        'recent_applications': recent_applications,
    }
    return render(request, 'dashboard/home.html', context)


@login_required
def manage_jobs(request):
    try:
        employer = request.user.employer_profile
    except Employer.DoesNotExist:
        messages.error(request, 'You are not registered as an employer.')
        return redirect('home')

    jobs = Job.objects.filter(employer=employer).order_by('-created_at')
    paginator = Paginator(jobs, 15)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)

    context = {'jobs': jobs}
    return render(request, 'dashboard/manage_jobs.html', context)


@login_required
def create_job(request):
    try:
        employer = request.user.employer_profile
    except Employer.DoesNotExist:
        messages.error(request, 'You are not registered as an employer.')
        return redirect('home')

    if request.method == 'POST':
        title = request.POST.get('title')
        location = request.POST.get('location')
        job_type = request.POST.get('job_type')
        industry = request.POST.get('industry')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        salary_min = request.POST.get('salary_min')
        salary_max = request.POST.get('salary_max')
        deadline = request.POST.get('deadline')

        Job.objects.create(
            employer=employer,
            title=title,
            location=location,
            job_type=job_type,
            industry=industry,
            description=description,
            requirements=requirements,
            salary_min=salary_min or None,
            salary_max=salary_max or None,
            deadline=deadline,
        )

        messages.success(request, 'Job posted successfully!')
        return redirect('manage_jobs')

    locations = Job._meta.get_field('location').choices
    job_types = Job._meta.get_field('job_type').choices
    industries = Job._meta.get_field('industry').choices

    context = {
        'locations': locations,
        'job_types': job_types,
        'industries': industries,
    }
    return render(request, 'dashboard/create_job.html', context)


@login_required
def edit_job(request, job_id):
    try:
        employer = request.user.employer_profile
        job = get_object_or_404(Job, id=job_id, employer=employer)
    except Employer.DoesNotExist:
        messages.error(request, 'You are not registered as an employer.')
        return redirect('home')

    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.location = request.POST.get('location')
        job.job_type = request.POST.get('job_type')
        job.industry = request.POST.get('industry')
        job.description = request.POST.get('description')
        job.requirements = request.POST.get('requirements')
        job.salary_min = request.POST.get('salary_min') or None
        job.salary_max = request.POST.get('salary_max') or None
        job.deadline = request.POST.get('deadline')
        job.is_active = request.POST.get('is_active') == 'on'
        job.save()

        messages.success(request, 'Job updated successfully!')
        return redirect('manage_jobs')

    locations = Job._meta.get_field('location').choices
    job_types = Job._meta.get_field('job_type').choices
    industries = Job._meta.get_field('industry').choices

    context = {
        'job': job,
        'locations': locations,
        'job_types': job_types,
        'industries': industries,
    }
    return render(request, 'dashboard/edit_job.html', context)


@login_required
def delete_job(request, job_id):
    try:
        employer = request.user.employer_profile
        job = get_object_or_404(Job, id=job_id, employer=employer)
    except Employer.DoesNotExist:
        messages.error(request, 'You are not registered as an employer.')
        return redirect('home')

    job.delete()
    messages.success(request, 'Job deleted successfully!')
    return redirect('manage_jobs')


@login_required
def view_applications(request, job_id):
    try:
        employer = request.user.employer_profile
        job = get_object_or_404(Job, id=job_id, employer=employer)
    except Employer.DoesNotExist:
        messages.error(request, 'You are not registered as an employer.')
        return redirect('home')

    applications = Applicant.objects.filter(job=job).order_by('-applied_at')

    context = {
        'job': job,
        'applications': applications,
    }
    return render(request, 'dashboard/view_applications.html', context)


@login_required
def edit_company_profile(request):
    try:
        employer = request.user.employer_profile
    except Employer.DoesNotExist:
        messages.error(request, 'You are not registered as an employer.')
        return redirect('home')

    if request.method == 'POST':
        employer.company_name = request.POST.get('company_name')
        employer.industry = request.POST.get('industry')
        employer.website = request.POST.get('website')
        employer.description = request.POST.get('description')
        if request.FILES.get('logo'):
            employer.logo = request.FILES.get('logo')
        employer.save()

        messages.success(request, 'Company profile updated!')
        return redirect('dashboard_home')

    context = {'employer': employer}
    return render(request, 'dashboard/edit_company.html', context)