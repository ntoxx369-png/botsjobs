from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from jobs.models import Employer, Job
from datetime import timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Seeds the database with sample jobs and employers'

    def handle(self, *args, **options):
        if Employer.objects.exists():
            self.stdout.write(self.style.WARNING('Database already has data. Skipping seed.'))
            return

        employer_user = User.objects.create_user(username='sample_employer', email='employer@sample.com', password='password123')
        employer = Employer.objects.create(
            user=employer_user,
            company_name='Botswana Tech Solutions',
            industry='IT',
            description='Leading IT solutions provider in Botswana.',
            is_verified=True
        )

        jobs_data = [
            {
                'title': 'Senior Software Developer',
                'location': 'gaborone',
                'job_type': 'full_time',
                'industry': 'it',
                'description': '''We are looking for an experienced Software Developer to join our growing team.

Responsibilities:
- Design, develop, and maintain web applications
- Write clean, maintainable, and efficient code
- Collaborate with cross-functional teams
- Mentor junior developers

What we offer:
- Competitive salary
- Flexible working hours
- Health insurance
- Professional development opportunities''',
                'requirements': '''Requirements:
- 5+ years of experience in software development
- Proficiency in Python, Django, or Node.js
- Experience with PostgreSQL or MySQL
- Strong problem-solving skills
- Good communication skills''',
                'salary_min': 25000,
                'salary_max': 40000,
                'deadline': timezone.now().date() + timedelta(days=30)
            },
            {
                'title': 'Marketing Manager',
                'location': 'gaborone',
                'job_type': 'full_time',
                'industry': 'media',
                'description': '''We are seeking a dynamic Marketing Manager to lead our marketing efforts.

Key Responsibilities:
- Develop and implement marketing strategies
- Manage social media accounts
- Analyze market trends
- Coordinate marketing campaigns''',
                'requirements': '''Requirements:
- 3+ years of marketing experience
- Bachelor's degree in Marketing or related field
- Experience with digital marketing
- Strong analytical skills''',
                'salary_min': 18000,
                'salary_max': 28000,
                'deadline': timezone.now().date() + timedelta(days=21)
            },
            {
                'title': 'Data Analyst Intern',
                'location': 'francistown',
                'job_type': 'internship',
                'industry': 'it',
                'description': '''Join our team as a Data Analyst Intern and gain hands-on experience.

What you will do:
- Analyze large datasets
- Create reports and visualizations
- Support data collection efforts
- Learn from experienced professionals''',
                'requirements': '''Requirements:
- Currently pursuing degree in Statistics, Computer Science, or related field
- Basic knowledge of Excel and SQL
- Strong attention to detail''',
                'salary_min': 5000,
                'salary_max': 8000,
                'deadline': timezone.now().date() + timedelta(days=14)
            },
            {
                'title': 'Mining Engineer',
                'location': 'orapa',
                'job_type': 'full_time',
                'industry': 'mining',
                'description': '''We are looking for an experienced Mining Engineer for our diamond mining operations.

Key Responsibilities:
- Plan and supervise mining operations
- Ensure safety compliance
- Optimize production efficiency
- Coordinate with geological teams''',
                'requirements': '''Requirements:
- Bachelor's degree in Mining Engineering
- 5+ years of mining experience
- Knowledge of mining software
- Valid driver's license''',
                'salary_min': 35000,
                'salary_max': 55000,
                'deadline': timezone.now().date() + timedelta(days=45)
            },
            {
                'title': 'Customer Service Representative',
                'location': 'maun',
                'job_type': 'part_time',
                'industry': 'retail',
                'description': '''We are hiring a Part-time Customer Service Representative for our growing tourism company.

Responsibilities:
- Handle customer inquiries
- Process bookings
- Maintain customer records
- Assist with office administration''',
                'requirements': '''Requirements:
- Matric certificate
- Friendly personality
- Basic computer skills
- Available weekends and holidays''',
                'salary_min': 6000,
                'salary_max': 10000,
                'deadline': timezone.now().date() + timedelta(days=10)
            },
            {
                'title': 'Remote UX Designer',
                'location': 'remote',
                'job_type': 'remote',
                'industry': 'it',
                'description': '''We are looking for a talented UX Designer to work remotely.

What you will do:
- Design user-friendly interfaces
- Conduct user research
- Create wireframes and prototypes
- Collaborate with development team''',
                'requirements': '''Requirements:
- 2+ years of UX design experience
- Proficiency in Figma or Sketch
- Portfolio demonstrating design skills
- Strong communication skills''',
                'salary_min': 30000,
                'salary_max': 45000,
                'deadline': timezone.now().date() + timedelta(days=20)
            },
        ]

        for job_data in jobs_data:
            Job.objects.create(employer=employer, **job_data)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(jobs_data)} sample jobs and 1 employer'))
        self.stdout.write(self.style.SUCCESS('Login with username: sample_employer, password: password123'))