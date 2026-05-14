from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Faculty, Department, StudyProgram, Application, ApplicationDocument, ExamResult, News, FAQ, Contact, DocumentTemplate


class StyledFormMixin:
    def apply_common_classes(self):
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault('class', 'form-check-input')
            else:
                widget.attrs.setdefault('class', 'form-control')


class CustomUserCreationForm(StyledFormMixin, UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'username': 'Логин',
            'password1': 'Пароль',
            'password2': 'Повторите пароль',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_common_classes()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'phone']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (___) ___-__-__'}),
        }


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name', 'short_name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['faculty', 'name', 'short_name', 'description', 'is_active']
        widgets = {
            'faculty': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class StudyProgramForm(forms.ModelForm):
    class Meta:
        model = StudyProgram
        fields = ['department', 'name', 'code', 'level', 'form', 'budget_places', 'paid_places', 'description', 'is_active']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'form': forms.Select(attrs={'class': 'form-control'}),
            'budget_places': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'paid_places': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['campaign', 'program', 'status', 'comment']
        widgets = {
            'campaign': forms.Select(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ApplicantApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['campaign', 'program', 'comment']
        widgets = {
            'campaign': forms.Select(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Можно указать вопросы или комментарии для приемной комиссии'}),
        }


class ApplicationDocumentForm(forms.ModelForm):
    class Meta:
        model = ApplicationDocument
        fields = ['doc_type', 'file']
        widgets = {
            'doc_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'data-file-input': 'true'}),
        }


class ExamResultForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = ['application', 'exam', 'score', 'notes']
        widgets = {
            'application': forms.Select(attrs={'class': 'form-control'}),
            'exam': forms.Select(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'slug', 'content', 'image', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'order', 'is_active']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'address', 'office_hours', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'office_hours': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DocumentTemplateForm(forms.ModelForm):
    class Meta:
        model = DocumentTemplate
        fields = ['name', 'file', 'doc_format', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'data-file-input': 'true'}),
            'doc_format': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
