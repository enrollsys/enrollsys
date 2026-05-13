from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import (
    UserProfile, Faculty, Department, StudyProgram,
    AdmissionCampaign, Application, ApplicationDocument,
    Exam, ExamResult, News, FAQ, Contact, DocumentTemplate
)
from .forms import (
    CustomUserCreationForm, UserProfileForm, FacultyForm, DepartmentForm,
    StudyProgramForm, ApplicationForm, ApplicationDocumentForm,
    ExamResultForm, NewsForm, FAQForm, ContactForm, DocumentTemplateForm
)


def home(request):
    latest_news = News.objects.filter(is_published=True)[:5]
    active_programs = StudyProgram.objects.filter(is_active=True)[:6]
    contacts = Contact.objects.filter(is_active=True)
    faqs = FAQ.objects.filter(is_active=True)[:5]
    context = {
        'news': latest_news,
        'programs': active_programs,
        'contacts': contacts,
        'faqs': faqs,
    }
    return render(request, 'core/home.html', context)


def news_list(request):
    news = News.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'core/news_list.html', {'news': news})


def news_detail(request, slug):
    article = get_object_or_404(News, slug=slug, is_published=True)
    return render(request, 'core/news_detail.html', {'article': article})


def program_list(request):
    programs = StudyProgram.objects.filter(is_active=True).select_related('department__faculty')
    return render(request, 'core/program_list.html', {'programs': programs})


def program_detail(request, pk):
    program = get_object_or_404(StudyProgram, pk=pk, is_active=True)
    exams = program.exams.filter(is_active=True)
    return render(request, 'core/program_detail.html', {'program': program, 'exams': exams})


def faculty_list(request):
    faculties = Faculty.objects.filter(is_active=True).prefetch_related('departments')
    return render(request, 'core/faculty_list.html', {'faculties': faculties})


def faq_list(request):
    faqs = FAQ.objects.filter(is_active=True).order_by('order', 'id')
    return render(request, 'core/faq_list.html', {'faqs': faqs})


def contact_list(request):
    contacts = Contact.objects.filter(is_active=True)
    return render(request, 'core/contact_list.html', {'contacts': contacts})


def campaign_list(request):
    campaigns = AdmissionCampaign.objects.filter(status='active').order_by('-year')
    return render(request, 'core/campaign_list.html', {'campaigns': campaigns})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, role='applicant')
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'core/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def applicant_dashboard(request):
    applications = Application.objects.filter(applicant=request.user).select_related('program', 'campaign')
    return render(request, 'core/applicant_dashboard.html', {'applications': applications})


@login_required
def application_create(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.applicant = request.user
            app.save()
            return redirect('applicant_dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'core/application_form.html', {'form': form})


@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk, applicant=request.user)
    documents = application.documents.all()
    return render(request, 'core/application_detail.html', {'application': application, 'documents': documents})
