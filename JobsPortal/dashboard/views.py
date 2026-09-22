from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from jobs.models import Job, Employer, Applicant, Gig, GigApplication, Payment
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


@login_required
def manage_gigs(request):
    gigs = Gig.objects.filter(poster=request.user).order_by('-created_at')
    paginator = Paginator(gigs, 15)
    page = request.GET.get('page')
    gigs = paginator.get_page(page)
    context = {'gigs': gigs}
    return render(request, 'dashboard/manage_gigs.html', context)


@login_required
def create_gig(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        location = request.POST.get('location')
        description = request.POST.get('description')
        budget_min = request.POST.get('budget_min')
        budget_max = request.POST.get('budget_max')
        deadline = request.POST.get('deadline')

        Gig.objects.create(
            poster=request.user,
            title=title,
            category=category,
            location=location,
            description=description,
            budget_min=budget_min or None,
            budget_max=budget_max or None,
            deadline=deadline,
        )

        messages.success(request, 'Gig posted successfully!')
        return redirect('manage_gigs')

    categories = Gig._meta.get_field('category').choices
    locations = Gig._meta.get_field('location').choices
    context = {'categories': categories, 'locations': locations}
    return render(request, 'dashboard/create_gig.html', context)


@login_required
def edit_gig(request, gig_id):
    gig = get_object_or_404(Gig, id=gig_id, poster=request.user)

    if request.method == 'POST':
        gig.title = request.POST.get('title')
        gig.category = request.POST.get('category')
        gig.location = request.POST.get('location')
        gig.description = request.POST.get('description')
        gig.budget_min = request.POST.get('budget_min') or None
        gig.budget_max = request.POST.get('budget_max') or None
        gig.deadline = request.POST.get('deadline')
        gig.status = request.POST.get('status', gig.status)
        gig.save()

        messages.success(request, 'Gig updated successfully!')
        return redirect('manage_gigs')

    categories = Gig._meta.get_field('category').choices
    locations = Gig._meta.get_field('location').choices
    context = {'gig': gig, 'categories': categories, 'locations': locations}
    return render(request, 'dashboard/edit_gig.html', context)


@login_required
def delete_gig(request, gig_id):
    gig = get_object_or_404(Gig, id=gig_id, poster=request.user)
    gig.delete()
    messages.success(request, 'Gig deleted successfully!')
    return redirect('manage_gigs')


@login_required
def view_gig_applications(request, gig_id):
    gig = get_object_or_404(Gig, id=gig_id, poster=request.user)
    applications = GigApplication.objects.filter(gig=gig).order_by('-applied_at')
    context = {'gig': gig, 'applications': applications}
    return render(request, 'dashboard/view_gig_applications.html', context)


@login_required
def featured_jobs(request):
    jobs = Job.objects.filter(employer=request.user.employer_profile, is_active=True).order_by('-created_at')
    payments = Payment.objects.filter(user=request.user, purpose='featured_job').order_by('-created_at')
    context = {
        'jobs': jobs,
        'payments': payments,
        'featured_price': 150,
    }
    return render(request, 'dashboard/featured_jobs.html', context)


@login_required
def upgrade_job(request, job_id):
    employer = get_object_or_404(Employer, user=request.user)
    job = get_object_or_404(Job, id=job_id, employer=employer)

    if request.method == 'POST':
        Payment.objects.create(
            user=request.user,
            purpose='featured_job',
            amount=150,
            currency='BWP',
            method='',
            reference='',
            status='pending',
        )
        job.is_featured = True
        job.save()
        messages.success(request, f'"{job.title}" is now featured! Payment is pending confirmation via MyZaka/Orange Money.')
        return redirect('featured_jobs')

    context = {'job': job}
    return render(request, 'dashboard/upgrade_job.html', context)