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
