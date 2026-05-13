from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('applicant', 'Абитуриент'),
        ('methodist', 'Методист'),
        ('admin', 'Администратор'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='applicant')
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


class Faculty(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название факультета')
    short_name = models.CharField(max_length=50, blank=True, verbose_name='Краткое название')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'
        ordering = ['name']


class Department(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments', verbose_name='Факультет')
    name = models.CharField(max_length=200, verbose_name='Название кафедры')
    short_name = models.CharField(max_length=50, blank=True, verbose_name='Краткое название')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Кафедра'
        verbose_name_plural = 'Кафедры'
        ordering = ['name']


class StudyProgram(models.Model):
    LEVEL_CHOICES = [
        ('bachelor', 'Бакалавриат'),
        ('master', 'Магистратура'),
        ('specialist', 'Специалитет'),
        ('postgraduate', 'Аспирантура'),
    ]
    FORM_CHOICES = [
        ('full_time', 'Очная'),
        ('part_time', 'Очно-заочная'),
        ('distance', 'Заочная'),
    ]
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programs', verbose_name='Кафедра')
    name = models.CharField(max_length=200, verbose_name='Название направления')
    code = models.CharField(max_length=20, verbose_name='Код направления')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, verbose_name='Уровень образования')
    form = models.CharField(max_length=20, choices=FORM_CHOICES, verbose_name='Форма обучения')
    budget_places = models.PositiveIntegerField(default=0, verbose_name='Бюджетные места')
    paid_places = models.PositiveIntegerField(default=0, verbose_name='Платные места')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активно')

    def __str__(self):
        return f"{self.code} {self.name}"

    class Meta:
        verbose_name = 'Направление обучения'
        verbose_name_plural = 'Направления обучения'
        ordering = ['code']
