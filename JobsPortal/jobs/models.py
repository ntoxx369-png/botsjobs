from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='employer_logos/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'Employer'
        verbose_name_plural = 'Employers'


class Job(models.Model):
    JOB_TYPES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    ]

    INDUSTRY_CHOICES = [
        ('it', 'IT & Technology'),
        ('finance', 'Finance & Banking'),
        ('mining', 'Mining & Energy'),
        ('tourism', 'Tourism & Hospitality'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('retail', 'Retail & Wholesale'),
        ('construction', 'Construction'),
        ('agriculture', 'Agriculture'),
        ('manufacturing', 'Manufacturing'),
        ('media', 'Media & Marketing'),
        ('legal', 'Legal'),
        ('other', 'Other'),
    ]

    LOCATION_CHOICES = [
        ('gaborone', 'Gaborone'),
        ('francistown', 'Francistown'),
        ('maun', 'Maun'),
        ('serowe', 'Serowe'),
        ('selibe_phikwe', 'Selibe Phikwe'),
        ('orapa', 'Orapa'),
        ('kanye', 'Kanye'),
        ('molepolole', 'Molepolole'),
        ('kweneng', 'Kweneng'),
        ('lobatse', 'Lobatse'),
        ('remote', 'Remote'),
        ('other', 'Other'),
    ]

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, default='gaborone')
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='full_time')
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, default='other')
    description = models.TextField()
    requirements = models.TextField()
    salary_min = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    salary_currency = models.CharField(max_length=3, default='BWP')
    deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.employer.company_name}"

    @property
    def application_count(self):
        return self.applications.count()


class Applicant(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume = models.FileField(upload_to='resumes/%Y/%m/')
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.job.title}"

    class Meta:
        verbose_name = 'Applicant'
        verbose_name_plural = 'Applicants'
        ordering = ['-applied_at']


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume')
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    headline = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    resume_file = models.FileField(upload_to='profile_resumes/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Resume'
        verbose_name_plural = 'Resumes'