from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect,get_object_or_404
from authentication.models import *
from .threads import *
from .models import *
from .forms import JobForm
from django.contrib import messages
from .models import JobModel
from django.http import HttpResponseRedirect
context = {}


# all companies page
def all_companies(request):
    context["companies"] = CompanyModel.objects.all()
    # context["companies"] = CompanyModel.objects.raw('SELECT * FROM company')
    return render(request, "main/all-companies.html", context)


# job single
@login_required(login_url='/student-login/')
def single_job(request, job_id):
    context["job"] = JobModel.objects.get(id=job_id)
    # context["job"] = JobModel.objects.raw(f"SELECT * FROM job where id={job_id}")
    return render(request, "student/job-desc.html", context)


# student dashboard
@login_required(login_url='/student-login/')
def student_dashboard(request):
    try:
        user = StudentModel.objects.get(email=request.user)
        context["jobs"] = JobModel.objects.filter(is_active=True).order_by("-created_at")
        # context["jobs"] = JobModel.objects.raw('SELECT * FROM job where is_active=true created_at dec')
        context["applications"] = JobApplicationModel.objects.filter(applicant=user)
    except Exception as e:
        print(e)
    return render(request, "dashboard/stu-dash.html", context)


# tpo dashboard
@login_required(login_url='/tpo-login/')
def tpo_dashboard(request):
    try:
        context["jobs"] = JobModel.objects.all().order_by("-created_at")
    except Exception as e:
        print(e)
    return render(request, "dashboard/tpo-dash.html", context)


def add_job(request):
    companies = CompanyModel.objects.all()
    print(companies)  # This will print the queryset in the console
    if request.method == 'POST':
        position = request.POST.get('position')
        company_id = request.POST.get('company')  # This will get the company ID from the form
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        last_apply_date = request.POST.get('last_apply_date')
        pay_rate = request.POST.get('pay_rate')
        max_applicant = request.POST.get('max_applicant')
        is_active = request.POST.get('is_active') == 'on'

        try:
            company = CompanyModel.objects.get(id=company_id)  # Fetch the company instance using ID
        except CompanyModel.DoesNotExist:
            messages.error(request, "Selected company does not exist.")
            return render(request, 'accounts/add_jobs.html', {'companies': companies})

        job = JobModel(
            position=position,
            company=company,
            description=description,
            requirements=requirements,
            last_apply_date=last_apply_date,
            pay_rate=pay_rate,
            max_applicant=max_applicant,
            is_active=is_active
        )
        job.save()

        messages.success(request, "Job added successfully!")
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/add_jobs.html', {'companies': companies})

def add_company(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        logo = request.FILES.get('logo')
        address = request.POST.get('address')
        desc = request.POST.get('desc')
        web_link = request.POST.get('web_link')

        if not company_name or not address or not web_link:
            messages.error(request, 'Some required fields are missing.')
            return redirect('add_company')

        new_company = CompanyModel(
            company_name=company_name,
            logo=logo,
            address=address,
            desc=desc,
            web_link=web_link
        )
        new_company.save()
        messages.success(request, 'Company added successfully!')
        return redirect('add_company')

    return render(request, 'accounts/add_company.html')


# tpo dashboard
@login_required(login_url='/tpo-login/')
def tpo_applicants_list(request, job_id):
    try:
        context["job_applicantion"] = JobApplicationModel.objects.filter(job__id=job_id)
    except Exception as e:
        print(e)
    return render(request, "tpo/applicants-list.html", context)


# Job Applicaition Accept
def tpo_accept_application(request, application_id):
    if request.method == 'POST':
        job_application = get_object_or_404(JobApplicationModel, id=application_id)
        job_application.status = 'Accepted'
        job_application.save()

        # Initiating email sending in a separate thread
        email_thread = send_result(job_application.applicant.email, job_application.job.position, 'accepted')
        email_thread.start()

        messages.success(request, "Application accepted successfully.")
        return redirect(request.META.get('HTTP_REFERER', 'default_redirect_url'))

    messages.error(request, "Invalid request.")
    return redirect(request.META.get('HTTP_REFERER', 'default_redirect_url'))


def tpo_reject_application(request, application_id):
    if request.method == 'POST':
        job_application = get_object_or_404(JobApplicationModel, id=application_id)
        job_application.status = 'Rejected'
        job_application.save()

        # Initiating email sending in a separate thread
        email_thread = send_result(job_application.applicant.email, job_application.job.position, 'rejected')
        email_thread.start()

        messages.success(request, "Application rejected successfully.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "Invalid request.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





# Apply for Job
@login_required(login_url='/student-login/')
def apply_for_job(request, job_id):
    try:
        user = StudentModel.objects.get(email=request.user)
        job =JobModel.objects.get(id=job_id)
        app_obj, _ = JobApplicationModel.objects.get_or_create(job=job, applicant=user, status="Applied")
        thread_obj = send_applied_mail(user.email, job.company.company_name, job.position)
        thread_obj.start()
        app_obj.save()
        return redirect("student-dashboard")
    except Exception as e:
        print(e)
    return render(request, "student/job-desc.html", context)
