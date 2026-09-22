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
    is_featured = models.BooleanField(default=False)
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


class Gig(models.Model):
    GIG_CATEGORIES = [
        ('delivery', 'Delivery & Transport'),
        ('tutoring', 'Tutoring & Education'),
        ('events', 'Events & Catering'),
        ('trades', 'Plumbing, Electrical & Trades'),
        ('cleaning', 'Cleaning & Maintenance'),
        ('it', 'IT & Digital'),
        ('creative', 'Design, Photo & Video'),
        ('agriculture', 'Farming & Agriculture'),
        ('retail', 'Retail & Sales'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gigs_posted')
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=GIG_CATEGORIES, default='other')
    description = models.TextField()
    location = models.CharField(max_length=50, choices=Job.LOCATION_CHOICES, default='gaborone')
    budget_min = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    budget_max = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    budget_currency = models.CharField(max_length=3, default='BWP')
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} (Gig)"

    @property
    def application_count(self):
        return self.gig_applications.count()

    class Meta:
        ordering = ['-created_at']


class GigApplication(models.Model):
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE, related_name='gig_applications')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    quote_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.gig.title}"

    class Meta:
        ordering = ['-applied_at']


class Payment(models.Model):
    PURPOSE_CHOICES = [
        ('featured_job', 'Featured Job Post'),
        ('featured_gig', 'Featured Gig Post'),
        ('subscription', 'Employer Subscription'),
        ('resume_spotlight', 'Resume Spotlight'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    purpose = models.CharField(max_length=30, choices=PURPOSE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='BWP')
    method = models.CharField(max_length=50, blank=True, help_text='e.g. MyZaka, Orange Money')
    reference = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_purpose_display()} - {self.get_status_display()}"

    class Meta:
        ordering = ['-created_at']


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