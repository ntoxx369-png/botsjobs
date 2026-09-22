from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from jobs.models import Applicant, Employer, Gig, GigApplication, Job


class Command(BaseCommand):
    help = 'Removes all demo/sample data. Real jobs and gigs are never touched.'

    def handle(self, *args, **options):
        demo_usernames = ['sample_employer', 'sample_gigger']
        demo_companies = ['Botswana Tech Solutions']
        demo_users = User.objects.filter(username__in=demo_usernames)
        demo_employers = Employer.objects.filter(
            user__in=demo_users
        ) | Employer.objects.filter(company_name__in=demo_companies)

        demo_jobs = Job.objects.filter(employer__in=demo_employers)
        demo_gigs = Gig.objects.filter(poster__in=demo_users)

        job_count = demo_jobs.count()
        gig_count = demo_gigs.count()

        Applicant.objects.filter(job__in=demo_jobs).delete()
        GigApplication.objects.filter(gig__in=demo_gigs).delete()
        demo_jobs.delete()
        demo_gigs.delete()
        demo_employers.delete()
        demo_users.delete()

        if job_count or gig_count:
            self.stdout.write(self.style.SUCCESS(
                f'Removed {job_count} demo jobs, {gig_count} demo gigs, and demo accounts.'
            ))
        else:
            self.stdout.write(self.style.SUCCESS('No demo data found. Database is clean.'))
