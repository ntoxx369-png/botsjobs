from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from jobs.models import Employer, Resume, Job, Applicant


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_type = request.POST.get('user_type')
        company_name = request.POST.get('company_name', '')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)

        if user_type == 'employer':
            Employer.objects.create(user=user, company_name=company_name or username)
        elif user_type == 'jobseeker':
            Resume.objects.create(user=user, full_name=username)

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('home')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    user = request.user
    is_employer = hasattr(user, 'employer_profile')
    resume = None
    applications = []
    jobs = []
    employer_profile = None

    if is_employer:
        employer_profile = user.employer_profile
        jobs = Job.objects.filter(employer=employer_profile).order_by('-created_at')
    else:
        try:
            resume = user.resume
        except Resume.DoesNotExist:
            resume = None
        applications = Applicant.objects.filter(email=user.email).order_by('-applied_at')[:10]

    context = {
        'user': user,
        'is_employer': is_employer,
        'resume': resume,
        'applications': applications,
        'jobs': jobs,
        'employer_profile': employer_profile,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_resume(request):
    try:
        resume = request.user.resume
    except Resume.DoesNotExist:
        resume = Resume.objects.create(user=request.user, full_name=request.user.username)

    if request.method == 'POST':
        resume.full_name = request.POST.get('full_name', resume.full_name)
        resume.phone = request.POST.get('phone', resume.phone)
        resume.headline = request.POST.get('headline', resume.headline)
        resume.summary = request.POST.get('summary', resume.summary)
        resume.skills = request.POST.get('skills', resume.skills)
        resume.experience = request.POST.get('experience', resume.experience)
        resume.education = request.POST.get('education', resume.education)
        if request.FILES.get('resume_file'):
            resume.resume_file = request.FILES.get('resume_file')
        resume.save()
        messages.success(request, 'Resume updated successfully.')
        return redirect('profile')

    return render(request, 'accounts/edit_resume.html', {'resume': resume})


def employer_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        company_name = request.POST.get('company_name')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('employer_register')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return redirect('employer_register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('employer_register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('employer_register')

        user = User.objects.create_user(username=username, email=email, password=password)
        Employer.objects.create(user=user, company_name=company_name or username)

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome! Your account is ready — post your first job now.')
            return redirect('create_job')

    return render(request, 'accounts/employer_register.html')