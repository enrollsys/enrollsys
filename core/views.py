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

