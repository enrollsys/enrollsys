import os
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import FileResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import (
    UserProfile, Faculty, Department, StudyProgram,
    AdmissionCampaign, Application, ApplicationDocument,
    Exam, ExamResult, News, FAQ, Contact, DocumentTemplate
)
from .forms import (
    CustomUserCreationForm, UserProfileForm, ApplicantApplicationForm,
    ApplicationForm, ApplicationDocumentForm, ExamResultForm
)
from .utils import generate_docx, generate_xlsx, serve_generated_file


def has_role(user, roles):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role in roles


def dashboard_redirect(user):
    if has_role(user, ['admin']):
        return 'admin_dashboard'
    if has_role(user, ['methodist']):
        return 'methodist_dashboard'
    return 'applicant_dashboard'


def public_stats():
    return {
        'programs_count': StudyProgram.objects.filter(is_active=True).count(),
        'faculties_count': Faculty.objects.filter(is_active=True).count(),
        'campaigns_count': AdmissionCampaign.objects.filter(status='active').count(),
        'faq_count': FAQ.objects.filter(is_active=True).count(),
    }


def home(request):
    context = public_stats()
    context.update({
        'news': News.objects.filter(is_published=True)[:3],
        'programs': StudyProgram.objects.filter(is_active=True).select_related('department__faculty')[:6],
        'campaigns': AdmissionCampaign.objects.filter(status='active')[:2],
        'breadcrumbs': [('Главная', None)],
        'page_title': 'Приемная комиссия',
    })
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html', {
        'breadcrumbs': [('Главная', 'home'), ('О сервисе', None)],
        'page_title': 'О сервисе',
    })


def admission_rules(request):
    return render(request, 'core/admission_rules.html', {
        'breadcrumbs': [('Главная', 'home'), ('Правила приема', None)],
        'page_title': 'Правила приема',
    })


def admission_documents(request):
    templates = DocumentTemplate.objects.filter(is_active=True)
    return render(request, 'core/admission_documents.html', {
        'templates': templates,
        'breadcrumbs': [('Главная', 'home'), ('Документы', None)],
        'page_title': 'Документы для поступления',
    })


def admission_schedule(request):
    exams = Exam.objects.filter(is_active=True).select_related('program').order_by('date')
    campaigns = AdmissionCampaign.objects.all()
    return render(request, 'core/admission_schedule.html', {
        'exams': exams,
        'campaigns': campaigns,
        'breadcrumbs': [('Главная', 'home'), ('Сроки приема', None)],
        'page_title': 'Сроки приема',
    })


def news_list(request):
    news = News.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'core/news_list.html', {
        'news': news,
        'breadcrumbs': [('Главная', 'home'), ('Новости', None)],
        'page_title': 'Новости',
    })


def news_detail(request, slug):
    article = get_object_or_404(News, slug=slug, is_published=True)
    return render(request, 'core/news_detail.html', {
        'article': article,
        'breadcrumbs': [('Главная', 'home'), ('Новости', 'news_list'), (article.title, None)],
        'page_title': article.title,
    })


def program_list(request):
    programs = StudyProgram.objects.filter(is_active=True).select_related('department__faculty')
    return render(request, 'core/program_list.html', {
        'programs': programs,
        'breadcrumbs': [('Главная', 'home'), ('Направления', None)],
        'page_title': 'Направления обучения',
    })


def program_detail(request, pk):
    program = get_object_or_404(StudyProgram.objects.select_related('department__faculty'), pk=pk, is_active=True)
    exams = program.exams.filter(is_active=True)
    return render(request, 'core/program_detail.html', {
        'program': program,
        'exams': exams,
        'breadcrumbs': [('Главная', 'home'), ('Направления', 'program_list'), (program.name, None)],
        'page_title': program.name,
    })


def faculty_list(request):
    faculties = Faculty.objects.filter(is_active=True).prefetch_related('departments__programs')
    return render(request, 'core/faculty_list.html', {
        'faculties': faculties,
        'breadcrumbs': [('Главная', 'home'), ('Факультеты', None)],
        'page_title': 'Факультеты',
    })


def faq_list(request):
    faqs = FAQ.objects.filter(is_active=True).order_by('order', 'id')
    return render(request, 'core/faq_list.html', {
        'faqs': faqs,
        'breadcrumbs': [('Главная', 'home'), ('FAQ', None)],
        'page_title': 'Вопросы и ответы',
    })


def contact_list(request):
    contacts = Contact.objects.filter(is_active=True)
    return render(request, 'core/contact_list.html', {
        'contacts': contacts,
        'breadcrumbs': [('Главная', 'home'), ('Контакты', None)],
        'page_title': 'Контакты',
    })


def campaign_list(request):
    campaigns = AdmissionCampaign.objects.all().order_by('-year')
    return render(request, 'core/campaign_list.html', {
        'campaigns': campaigns,
        'breadcrumbs': [('Главная', 'home'), ('Приемная кампания', None)],
        'page_title': 'Приемная кампания',
    })


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, role='applicant')
            login(request, user)
            messages.success(request, 'Аккаунт создан. Можно подать заявку.')
            return redirect('applicant_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {
        'form': form,
        'breadcrumbs': [('Главная', 'home'), ('Регистрация', None)],
        'page_title': 'Регистрация',
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(dashboard_redirect(user))
        messages.error(request, 'Неверный логин или пароль.')
    return render(request, 'core/login.html', {
        'breadcrumbs': [('Главная', 'home'), ('Вход', None)],
        'page_title': 'Вход',
    })


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def applicant_dashboard(request):
    applications = Application.objects.filter(applicant=request.user).select_related('program', 'campaign')
    documents = ApplicationDocument.objects.filter(application__applicant=request.user)
    results = ExamResult.objects.filter(application__applicant=request.user).select_related('exam', 'application__program')
    return render(request, 'core/applicant_dashboard.html', {
        'applications': applications,
        'documents': documents,
        'results': results,
        'breadcrumbs': [('Главная', 'home'), ('Кабинет абитуриента', None)],
        'page_title': 'Кабинет абитуриента',
    })


@login_required
def applicant_applications(request):
    applications = Application.objects.filter(applicant=request.user).select_related('program', 'campaign')
    return render(request, 'core/applicant_applications.html', {
        'applications': applications,
        'breadcrumbs': [('Главная', 'home'), ('Кабинет', 'applicant_dashboard'), ('Мои заявки', None)],
        'page_title': 'Мои заявки',
    })


@login_required
def applicant_documents(request):
    documents = ApplicationDocument.objects.filter(application__applicant=request.user).select_related('application__program')
    return render(request, 'core/applicant_documents.html', {
        'documents': documents,
        'breadcrumbs': [('Главная', 'home'), ('Кабинет', 'applicant_dashboard'), ('Документы', None)],
        'page_title': 'Мои документы',
    })


@login_required
def applicant_results(request):
    results = ExamResult.objects.filter(application__applicant=request.user).select_related('exam', 'application__program')
    return render(request, 'core/applicant_results.html', {
        'results': results,
        'breadcrumbs': [('Главная', 'home'), ('Кабинет', 'applicant_dashboard'), ('Результаты', None)],
        'page_title': 'Результаты',
    })


@login_required
def profile_edit(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            saved = form.save(commit=False)
            if profile.role == 'applicant':
                saved.role = 'applicant'
            saved.save()
            messages.success(request, 'Профиль обновлен.')
            return redirect('profile_edit')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'core/profile_edit.html', {
        'form': form,
        'breadcrumbs': [('Главная', 'home'), ('Профиль', None)],
        'page_title': 'Профиль',
    })


@login_required
def application_create(request):
    if request.method == 'POST':
        form = ApplicantApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.applicant = request.user
            app.status = 'submitted'
            app.save()
            messages.success(request, 'Заявка отправлена в управление приема.')
            return redirect('application_detail', pk=app.pk)
    else:
        form = ApplicantApplicationForm()
    return render(request, 'core/application_form.html', {
        'form': form,
        'breadcrumbs': [('Главная', 'home'), ('Кабинет', 'applicant_dashboard'), ('Новая заявка', None)],
        'page_title': 'Новая заявка',
    })


@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application.objects.select_related('program', 'campaign'), pk=pk, applicant=request.user)
    documents = application.documents.all()
    results = application.exam_results.select_related('exam')
    return render(request, 'core/application_detail.html', {
        'application': application,
        'documents': documents,
        'results': results,
        'breadcrumbs': [('Главная', 'home'), ('Кабинет', 'applicant_dashboard'), ('Мои заявки', 'applicant_applications'), (f'Заявка #{application.pk}', None)],
        'page_title': f'Заявка #{application.pk}',
    })


@login_required
def methodist_dashboard(request):
    if not has_role(request.user, ['methodist', 'admin']):
        return redirect('home')
    applications = Application.objects.filter(status__in=['submitted', 'under_review']).select_related('applicant', 'program', 'campaign')
    return render(request, 'core/methodist_dashboard.html', {
        'applications': applications,
        'breadcrumbs': [('Главная', 'home'), ('Кабинет методиста', None)],
        'page_title': 'Кабинет методиста',
    })


@login_required
def methodist_applications(request):
    if not has_role(request.user, ['methodist', 'admin']):
        return redirect('home')
    applications = Application.objects.all().select_related('applicant', 'program', 'campaign')
    return render(request, 'core/methodist_applications.html', {
        'applications': applications,
        'breadcrumbs': [('Главная', 'home'), ('Кабинет методиста', 'methodist_dashboard'), ('Заявки', None)],
        'page_title': 'Заявки абитуриентов',
    })


@login_required
def methodist_documents(request):
    if not has_role(request.user, ['methodist', 'admin']):
        return redirect('home')
    documents = ApplicationDocument.objects.select_related('application__applicant', 'application__program')
    return render(request, 'core/methodist_documents.html', {
        'documents': documents,
        'breadcrumbs': [('Главная', 'home'), ('Кабинет методиста', 'methodist_dashboard'), ('Документы', None)],
        'page_title': 'Документы заявок',
    })


@login_required
def methodist_templates(request):
    if not has_role(request.user, ['methodist', 'admin']):
        return redirect('home')
    templates = DocumentTemplate.objects.all()
    return render(request, 'core/methodist_templates.html', {
        'templates': templates,
        'breadcrumbs': [('Главная', 'home'), ('Кабинет методиста', 'methodist_dashboard'), ('Шаблоны', None)],
        'page_title': 'Шаблоны документов',
    })


@login_required
def admin_dashboard(request):
    if not has_role(request.user, ['admin']):
        return redirect('home')
    stats = {
        'total_users': User.objects.count(),
        'total_applications': Application.objects.count(),
        'active_programs': StudyProgram.objects.filter(is_active=True).count(),
        'active_campaigns': AdmissionCampaign.objects.filter(status='active').count(),
        'documents': ApplicationDocument.objects.count(),
    }
    return render(request, 'core/admin_dashboard.html', {
        'stats': stats,
        'breadcrumbs': [('Главная', 'home'), ('Панель администратора', None)],
        'page_title': 'Панель администратора',
    })


@login_required
def admin_users(request):
    if not has_role(request.user, ['admin']):
        return redirect('home')
    users = User.objects.select_related('profile').order_by('username')
    return render(request, 'core/admin_users.html', {
        'users': users,
        'breadcrumbs': [('Главная', 'home'), ('Администратор', 'admin_dashboard'), ('Пользователи', None)],
        'page_title': 'Пользователи',
    })


@login_required
def admin_applications(request):
    if not has_role(request.user, ['admin']):
        return redirect('home')
    applications = Application.objects.all().select_related('applicant', 'program', 'campaign')
    return render(request, 'core/admin_applications.html', {
        'applications': applications,
        'breadcrumbs': [('Главная', 'home'), ('Администратор', 'admin_dashboard'), ('Заявки', None)],
        'page_title': 'Заявки',
    })


@login_required
def admin_programs(request):
    if not has_role(request.user, ['admin']):
        return redirect('home')
    programs = StudyProgram.objects.all().select_related('department__faculty')
    return render(request, 'core/admin_programs.html', {
        'programs': programs,
        'breadcrumbs': [('Главная', 'home'), ('Администратор', 'admin_dashboard'), ('Направления', None)],
        'page_title': 'Направления',
    })


@login_required
def admin_campaigns(request):
    if not has_role(request.user, ['admin']):
        return redirect('home')
    campaigns = AdmissionCampaign.objects.all()
    return render(request, 'core/admin_campaigns.html', {
        'campaigns': campaigns,
        'breadcrumbs': [('Главная', 'home'), ('Администратор', 'admin_dashboard'), ('Кампании', None)],
        'page_title': 'Приемные кампании',
    })


@login_required
def admin_reports(request):
    if not has_role(request.user, ['admin']):
        return redirect('home')
    generated_dir = Path(settings.MEDIA_ROOT) / 'generated'
    files = []
    if generated_dir.exists():
        files = [
            {'name': item.name, 'size': item.stat().st_size}
            for item in sorted(generated_dir.iterdir(), key=lambda item: item.stat().st_mtime, reverse=True)
            if item.is_file()
        ]
    return render(request, 'core/admin_reports.html', {
        'files': files,
        'breadcrumbs': [('Главная', 'home'), ('Администратор', 'admin_dashboard'), ('Отчеты', None)],
        'page_title': 'Отчеты',
    })


@login_required
def application_review(request, pk):
    if not has_role(request.user, ['methodist', 'admin']):
        return redirect('home')
    application = get_object_or_404(Application.objects.select_related('applicant', 'program', 'campaign'), pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заявка обновлена.')
            return redirect('methodist_applications')
    else:
        form = ApplicationForm(instance=application)
    return render(request, 'core/application_review.html', {
        'form': form,
        'application': application,
        'documents': application.documents.all(),
        'breadcrumbs': [('Главная', 'home'), ('Заявки', 'methodist_applications'), (f'Проверка #{application.pk}', None)],
        'page_title': f'Проверка заявки #{application.pk}',
    })


@login_required
def document_upload(request, application_id):
    application = get_object_or_404(Application, pk=application_id, applicant=request.user)
    if request.method == 'POST':
        form = ApplicationDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.application = application
            doc.save()
            messages.success(request, 'Документ загружен.')
            return redirect('application_detail', pk=application_id)
    else:
        form = ApplicationDocumentForm()
    return render(request, 'core/document_upload.html', {
        'form': form,
        'application': application,
        'breadcrumbs': [('Главная', 'home'), ('Кабинет', 'applicant_dashboard'), (f'Заявка #{application.pk}', None), ('Загрузка документа', None)],
        'page_title': 'Загрузка документа',
    })


@login_required
def exam_result_create(request):
    if not has_role(request.user, ['methodist', 'admin']):
        return redirect('home')
    if request.method == 'POST':
        form = ExamResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.recorded_by = request.user
            result.save()
            messages.success(request, 'Результат экзамена сохранен.')
            return redirect('methodist_dashboard')
    else:
        form = ExamResultForm()
    return render(request, 'core/exam_result_form.html', {
        'form': form,
        'breadcrumbs': [('Главная', 'home'), ('Кабинет методиста', 'methodist_dashboard'), ('Результат экзамена', None)],
        'page_title': 'Добавить результат',
    })


@login_required
def export_application_docx(request, pk):
    application = get_object_or_404(Application.objects.select_related('applicant', 'program', 'campaign'), pk=pk)
    if application.applicant != request.user and not has_role(request.user, ['methodist', 'admin']):
        return HttpResponseForbidden('Нет доступа к документу.')
    content = '\n'.join([
        f'Заявка: #{application.pk}',
        f'Абитуриент: {application.applicant.get_full_name() or application.applicant.username}',
        f'Email: {application.applicant.email}',
        f'Направление: {application.program}',
        f'Кампания: {application.campaign}',
        f'Статус: {application.get_status_display()}',
        f'Дата: {timezone.localtime(application.created_at).strftime("%d.%m.%Y %H:%M")}',
        f'Комментарий: {application.comment or "Без комментария"}',
    ])
    path = generate_docx('Заявление абитуриента', content, f'application_{application.pk}.docx')
    return serve_generated_file(path)


@login_required
def export_applications_xlsx(request):
    if not has_role(request.user, ['methodist', 'admin']):
        return redirect('home')
    rows = []
    for app in Application.objects.select_related('applicant', 'program', 'campaign'):
        rows.append([
            app.pk,
            app.applicant.get_full_name() or app.applicant.username,
            app.applicant.email,
            app.program.code,
            app.program.name,
            app.campaign.year,
            app.get_status_display(),
            timezone.localtime(app.created_at).strftime('%d.%m.%Y %H:%M'),
        ])
    path = generate_xlsx(['ID', 'Абитуриент', 'Email', 'Код', 'Направление', 'Год', 'Статус', 'Создана'], rows, 'applications_register.xlsx')
    return serve_generated_file(path)


@login_required
def download_document(request, pk):
    document = get_object_or_404(ApplicationDocument.objects.select_related('application'), pk=pk)
    if document.application.applicant != request.user and not has_role(request.user, ['methodist', 'admin']):
        return HttpResponseForbidden('Нет доступа к файлу.')
    if not document.file:
        raise Http404('Файл не найден.')
    return FileResponse(document.file.open('rb'), as_attachment=True, filename=os.path.basename(document.file.name))


@login_required
def download_generated(request, filename):
    if not has_role(request.user, ['methodist', 'admin']):
        return redirect('home')
    generated_dir = Path(settings.MEDIA_ROOT) / 'generated'
    filepath = generated_dir / filename
    if not filepath.exists() or generated_dir.resolve() not in filepath.resolve().parents:
        raise Http404('Файл не найден.')
    return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)
