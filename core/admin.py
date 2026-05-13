from django.contrib import admin
from .models import (
    UserProfile, Faculty, Department, StudyProgram,
    AdmissionCampaign, Application, ApplicationDocument,
    Exam, ExamResult, News, FAQ, Contact, DocumentTemplate
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'short_name')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty', 'short_name', 'is_active')
    list_filter = ('faculty', 'is_active')
    search_fields = ('name', 'short_name')


@admin.register(StudyProgram)
class StudyProgramAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department', 'level', 'form', 'budget_places', 'paid_places', 'is_active')
    list_filter = ('level', 'form', 'is_active')
    search_fields = ('code', 'name')


@admin.register(AdmissionCampaign)
class AdmissionCampaignAdmin(admin.ModelAdmin):
    list_display = ('year', 'start_date', 'end_date', 'status')
    list_filter = ('status',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'applicant', 'program', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'campaign')
    search_fields = ('applicant__username', 'applicant__email')
    date_hierarchy = 'created_at'


@admin.register(ApplicationDocument)
class ApplicationDocumentAdmin(admin.ModelAdmin):
    list_display = ('doc_type', 'application', 'uploaded_at', 'is_verified')
    list_filter = ('doc_type', 'is_verified')


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'program', 'exam_type', 'date', 'max_score')
    list_filter = ('exam_type',)
    search_fields = ('name',)


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('application', 'exam', 'score', 'recorded_at', 'recorded_by')
    list_filter = ('exam',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at', 'author')
    list_filter = ('is_published',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('question',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'email')


@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'doc_format', 'created_at', 'is_active')
    list_filter = ('doc_format', 'is_active')
    search_fields = ('name',)

