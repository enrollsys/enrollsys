import shutil
import tempfile
from datetime import date

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import (
    AdmissionCampaign,
    Application,
    ApplicationDocument,
    Contact,
    Department,
    Exam,
    FAQ,
    Faculty,
    News,
    StudyProgram,
    UserProfile,
)


TEST_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class PublicSiteAndCabinetTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.faculty = Faculty.objects.create(name='Факультет экономики', short_name='ФЭ')
        self.department = Department.objects.create(faculty=self.faculty, name='Кафедра управления')
        self.program = StudyProgram.objects.create(
            department=self.department,
            name='Менеджмент',
            code='38.03.02',
            level='bachelor',
            form='full_time',
            budget_places=10,
            paid_places=50,
        )
        self.campaign = AdmissionCampaign.objects.create(
            year=2026,
            start_date=date(2026, 6, 1),
            end_date=date(2026, 8, 25),
            status='active',
        )
        self.news = News.objects.create(title='Старт приема', slug='start', content='Прием документов открыт.')
        FAQ.objects.create(question='Как подать заявку?', answer='Через личный кабинет.', is_active=True)
        Contact.objects.create(name='Приемная комиссия', email='admission@example.com', is_active=True)
        Exam.objects.create(program=self.program, name='Русский язык', exam_type='written', date=date(2026, 7, 1))

        self.applicant = User.objects.create_user('applicant', password='pass12345', email='a@example.com')
        UserProfile.objects.create(user=self.applicant, role='applicant')
        self.methodist = User.objects.create_user('methodist', password='pass12345', email='m@example.com')
        UserProfile.objects.create(user=self.methodist, role='methodist')
        self.admin = User.objects.create_user('admin', password='pass12345', email='admin@example.com')
        UserProfile.objects.create(user=self.admin, role='admin')
        self.application = Application.objects.create(
            applicant=self.applicant,
            campaign=self.campaign,
            program=self.program,
            status='submitted',
        )

    def test_public_pages_are_available_with_breadcrumbs(self):
        urls = [
            reverse('home'),
            reverse('about'),
            reverse('admission_rules'),
            reverse('program_list'),
            reverse('program_detail', args=[self.program.pk]),
            reverse('faculty_list'),
            reverse('campaign_list'),
            reverse('admission_schedule'),
            reverse('admission_documents'),
            reverse('news_list'),
            reverse('news_detail', args=[self.news.slug]),
            reverse('faq_list'),
            reverse('contact_list'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, url)
            self.assertContains(response, 'Хлебные крошки')

    def test_applicant_cabinet_pages_are_private(self):
        self.assertEqual(self.client.get(reverse('applicant_dashboard')).status_code, 302)
        self.client.login(username='applicant', password='pass12345')
        for name in ['applicant_dashboard', 'applicant_applications', 'applicant_documents', 'applicant_results', 'profile_edit']:
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200, name)

    def test_methodist_and_admin_role_access(self):
        self.client.login(username='methodist', password='pass12345')
        self.assertEqual(self.client.get(reverse('methodist_dashboard')).status_code, 200)
        self.assertEqual(self.client.get(reverse('admin_dashboard')).status_code, 302)
        self.client.logout()
        self.client.login(username='admin', password='pass12345')
        for name in ['admin_dashboard', 'admin_users', 'admin_applications', 'admin_programs', 'admin_campaigns', 'admin_reports']:
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200, name)

    def test_document_upload_and_download(self):
        self.client.login(username='applicant', password='pass12345')
        upload = SimpleUploadedFile('passport.txt', b'passport data', content_type='text/plain')
        response = self.client.post(reverse('document_upload', args=[self.application.pk]), {'doc_type': 'passport', 'file': upload})
        self.assertEqual(response.status_code, 302)
        document = ApplicationDocument.objects.get()
        response = self.client.get(reverse('download_document', args=[document.pk]))
        self.assertEqual(response.status_code, 200)

    def test_docx_and_xlsx_exports(self):
        self.client.login(username='applicant', password='pass12345')
        response = self.client.get(reverse('export_application_docx', args=[self.application.pk]))
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        self.client.login(username='admin', password='pass12345')
        response = self.client.get(reverse('export_applications_xlsx'))
        self.assertEqual(response.status_code, 200)
