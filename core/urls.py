from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('programs/', views.program_list, name='program_list'),
    path('programs/<int:pk>/', views.program_detail, name='program_detail'),
    path('faculties/', views.faculty_list, name='faculty_list'),
    path('faq/', views.faq_list, name='faq_list'),
    path('contacts/', views.contact_list, name='contact_list'),
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/applicant/', views.applicant_dashboard, name='applicant_dashboard'),
    path('dashboard/methodist/', views.methodist_dashboard, name='methodist_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('applications/create/', views.application_create, name='application_create'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/<int:pk>/review/', views.application_review, name='application_review'),
    path('applications/<int:application_id>/upload/', views.document_upload, name='document_upload'),
    path('exam-results/create/', views.exam_result_create, name='exam_result_create'),
]
