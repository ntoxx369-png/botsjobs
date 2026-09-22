from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from jobs.models import Employer, Job, Gig
from datetime import timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Seeds the database with sample jobs, gigs, and employers'

    def handle(self, *args, **options):
        if Gig.objects.exists():
            self.stdout.write(self.style.WARNING('Gigs already exist. Skipping.'))
            return

        employer_user = None
        if Employer.objects.exists():
            employer_user = Employer.objects.first().user
            self.stdout.write(self.style.WARNING('Employer exists. Reusing.'))
        else:
            employer_user = User.objects.create_user(username='sample_employer', email='employer@sample.com', password='password123')
            Employer.objects.create(
                user=employer_user,
                company_name='Botswana Tech Solutions',
                industry='IT',
                description='Leading IT solutions provider in Botswana.',
                is_verified=True
            )

        if not Job.objects.exists():
            jobs_data = [
                {
                    'title': 'Senior Software Developer',
                    'location': 'gaborone',
                    'job_type': 'full_time',
                    'industry': 'it',
                    'description': 'We are looking for an experienced Software Developer to join our growing team.\n\nResponsibilities:\n- Design, develop, and maintain web applications\n- Write clean, maintainable, and efficient code\n- Collaborate with cross-functional teams\n- Mentor junior developers\n\nWhat we offer:\n- Competitive salary\n- Flexible working hours\n- Health insurance\n- Professional development opportunities',
                    'requirements': 'Requirements:\n- 5+ years of experience in software development\n- Proficiency in Python, Django, or Node.js\n- Experience with PostgreSQL or MySQL\n- Strong problem-solving skills\n- Good communication skills',
                    'salary_min': 25000,
                    'salary_max': 40000,
                    'deadline': timezone.now().date() + timedelta(days=30)
                },
                {
                    'title': 'Marketing Manager',
                    'location': 'gaborone',
                    'job_type': 'full_time',
                    'industry': 'media',
                    'description': 'We are seeking a dynamic Marketing Manager to lead our marketing efforts.\n\nKey Responsibilities:\n- Develop and implement marketing strategies\n- Manage social media accounts\n- Analyze market trends\n- Coordinate marketing campaigns',
                    'requirements': 'Requirements:\n- 3+ years of marketing experience\n- Bachelor\'s degree in Marketing or related field\n- Experience with digital marketing\n- Strong analytical skills',
                    'salary_min': 18000,
                    'salary_max': 28000,
                    'deadline': timezone.now().date() + timedelta(days=21)
                },
                {
                    'title': 'Data Analyst Intern',
                    'location': 'francistown',
                    'job_type': 'internship',
                    'industry': 'it',
                    'description': 'Join our team as a Data Analyst Intern and gain hands-on experience.\n\nWhat you will do:\n- Analyze large datasets\n- Create reports and visualizations\n- Support data collection efforts\n- Learn from experienced professionals',
                    'requirements': 'Requirements:\n- Currently pursuing degree in Statistics, Computer Science, or related field\n- Basic knowledge of Excel and SQL\n- Strong attention to detail',
                    'salary_min': 5000,
                    'salary_max': 8000,
                    'deadline': timezone.now().date() + timedelta(days=14)
                },
                {
                    'title': 'Mining Engineer',
                    'location': 'orapa',
                    'job_type': 'full_time',
                    'industry': 'mining',
                    'description': 'We are looking for an experienced Mining Engineer for our diamond mining operations.\n\nKey Responsibilities:\n- Plan and supervise mining operations\n- Ensure safety compliance\n- Optimize production efficiency\n- Coordinate with geological teams',
                    'requirements': 'Requirements:\n- Bachelor\'s degree in Mining Engineering\n- 5+ years of mining experience\n- Knowledge of mining software\n- Valid driver\'s license',
                    'salary_min': 35000,
                    'salary_max': 55000,
                    'deadline': timezone.now().date() + timedelta(days=45)
                },
                {
                    'title': 'Customer Service Representative',
                    'location': 'maun',
                    'job_type': 'part_time',
                    'industry': 'retail',
                    'description': 'We are hiring a Part-time Customer Service Representative for our growing tourism company.\n\nResponsibilities:\n- Handle customer inquiries\n- Process bookings\n- Maintain customer records\n- Assist with office administration',
                    'requirements': 'Requirements:\n- Matric certificate\n- Friendly personality\n- Basic computer skills\n- Available weekends and holidays',
                    'salary_min': 6000,
                    'salary_max': 10000,
                    'deadline': timezone.now().date() + timedelta(days=10)
                },
                {
                    'title': 'Remote UX Designer',
                    'location': 'remote',
                    'job_type': 'remote',
                    'industry': 'it',
                    'description': 'We are looking for a talented UX Designer to work remotely.\n\nWhat you will do:\n- Design user-friendly interfaces\n- Conduct user research\n- Create wireframes and prototypes\n- Collaborate with development team',
                    'requirements': 'Requirements:\n- 2+ years of UX design experience\n- Proficiency in Figma or Sketch\n- Portfolio demonstrating design skills\n- Strong communication skills',
                    'salary_min': 30000,
                    'salary_max': 45000,
                    'deadline': timezone.now().date() + timedelta(days=20)
                },
            ]
            employer = Employer.objects.first()
            for job_data in jobs_data:
                Job.objects.create(employer=employer, **job_data)
            self.stdout.write(self.style.SUCCESS(f'Created {len(jobs_data)} jobs'))

        gig_user = User.objects.filter(username='sample_gigger').first()
        if not gig_user:
            gig_user = User.objects.create_user(username='sample_gigger', email='gigger@sample.com', password='password123')

        gigs_data = [
            {
                'poster': gig_user,
                'title': 'Weekend Delivery Driver Needed in Gaborone',
                'category': 'delivery',
                'location': 'gaborone',
                'description': 'Looking for a reliable person to deliver packages around Gaborone this Saturday and Sunday.\n\n- Own vehicle or bicycle required\n- Fuel allowance provided\n- Flexible hours (8am - 4pm)',
                'budget_min': 400,
                'budget_max': 700,
                'deadline': timezone.now().date() + timedelta(days=7),
            },
            {
                'poster': gig_user,
                'title': 'Math Tutor for Grade 10 Student (Ongoing)',
                'category': 'tutoring',
                'location': 'gaborone',
                'description': 'Seeking a patient math tutor for a Grade 10 student.\n\n- Twice a week (Tue & Thu, 4pm-6pm)\n- BGCSE curriculum\n- Tutoring center in Broadhurst',
                'budget_min': 200,
                'budget_max': 400,
                'deadline': timezone.now().date() + timedelta(days=14),
            },
            {
                'poster': gig_user,
                'title': 'Wedding Photographer for December Event',
                'category': 'creative',
                'location': 'francistown',
                'description': 'Need a professional photographer for a wedding on December 20th in Francistown.\n\n- Full day coverage (8am-8pm)\n- Edited digital photos\n- 2 photographers preferred',
                'budget_min': 3000,
                'budget_max': 6000,
                'deadline': timezone.now().date() + timedelta(days=60),
            },
            {
                'poster': gig_user,
                'title': 'Electrician for Office Renovation',
                'category': 'trades',
                'location': 'gaborone',
                'description': 'Need a qualified electrician for a small office renovation in Gaborone CBD.\n\n- Rewiring and new outlets\n- LED lighting installation\n- Estimated 3-5 days work',
                'budget_min': 2500,
                'budget_max': 5000,
                'deadline': timezone.now().date() + timedelta(days=21),
            },
            {
                'poster': gig_user,
                'title': 'Social Media Manager for Local Restaurant',
                'category': 'it',
                'location': 'gaborone',
                'description': 'Restaurant in Gaborone looking for someone to manage social media accounts.\n\n- Instagram, Facebook, TikTok\n- 3 posts per week\n- Basic photo editing',
                'budget_min': 1500,
                'budget_max': 3000,
                'deadline': timezone.now().date() + timedelta(days=14),
            },
            {
                'poster': gig_user,
                'title': 'Farm Helper Needed for Harvest Season',
                'category': 'agriculture',
                'location': 'kweneng',
                'description': 'Small farm in Kanye area needs help with harvest.\n\n- 2 weeks work\n- Accommodation and meals provided\n- Morning shifts (6am-2pm)',
                'budget_min': 800,
                'budget_max': 1200,
                'deadline': timezone.now().date() + timedelta(days=10),
            },
        ]

        created = 0
        for gig_data in gigs_data:
            Gig.objects.create(**gig_data)
            created += 1

        self.stdout.write(self.style.SUCCESS(f'Created {created} sample gigs'))
        self.stdout.write(self.style.SUCCESS('Demo accounts: sample_employer/password123, sample_gigger/password123'))