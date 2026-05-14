from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('applicant', 'Абитуриент'),
        ('methodist', 'Методист'),
        ('admin', 'Администратор'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='applicant', verbose_name='Роль')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

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


class AdmissionCampaign(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Запланирована'),
        ('active', 'Активна'),
        ('closed', 'Закрыта'),
    ]
    year = models.PositiveIntegerField(verbose_name='Учебный год')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned', verbose_name='Статус')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return f"Приемная кампания {self.year}"

    class Meta:
        verbose_name = 'Приемная кампания'
        verbose_name_plural = 'Приемные кампании'
        ordering = ['-year']


class Application(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('submitted', 'Подана'),
        ('under_review', 'На рассмотрении'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications', verbose_name='Абитуриент')
    campaign = models.ForeignKey(AdmissionCampaign, on_delete=models.CASCADE, related_name='applications', verbose_name='Кампания')
    program = models.ForeignKey(StudyProgram, on_delete=models.CASCADE, related_name='applications', verbose_name='Направление')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    def __str__(self):
        return f"Заявка #{self.id} от {self.applicant.username}"

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']


class ApplicationDocument(models.Model):
    DOC_TYPE_CHOICES = [
        ('passport', 'Паспорт'),
        ('diploma', 'Диплом/аттестат'),
        ('photo', 'Фотография'),
        ('certificate', 'Сертификат/документ'),
        ('other', 'Другое'),
    ]
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents', verbose_name='Заявка')
    doc_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES, verbose_name='Тип документа')
    file = models.FileField(upload_to='applications/%Y/%m/', verbose_name='Файл')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    is_verified = models.BooleanField(default=False, verbose_name='Проверен')

    def __str__(self):
        return f"{self.get_doc_type_display()} для заявки #{self.application.id}"

    class Meta:
        verbose_name = 'Документ заявки'
        verbose_name_plural = 'Документы заявок'
        ordering = ['-uploaded_at']


class Exam(models.Model):
    TYPE_CHOICES = [
        ('written', 'Письменный'),
        ('oral', 'Устный'),
        ('combined', 'Комбинированный'),
    ]
    program = models.ForeignKey(StudyProgram, on_delete=models.CASCADE, related_name='exams', verbose_name='Направление')
    name = models.CharField(max_length=200, verbose_name='Название экзамена')
    exam_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Тип экзамена')
    date = models.DateField(verbose_name='Дата проведения')
    location = models.CharField(max_length=200, blank=True, verbose_name='Место проведения')
    max_score = models.PositiveIntegerField(default=100, verbose_name='Максимальный балл')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Экзамен'
        verbose_name_plural = 'Экзамены'
        ordering = ['date']


class ExamResult(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='exam_results', verbose_name='Заявка')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results', verbose_name='Экзамен')
    score = models.PositiveIntegerField(verbose_name='Балл')
    notes = models.TextField(blank=True, verbose_name='Примечания')
    recorded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата записи')
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='recorded_results', verbose_name='Кто записал')

    def __str__(self):
        return f"{self.exam.name}: {self.score}"

    class Meta:
        verbose_name = 'Результат экзамена'
        verbose_name_plural = 'Результаты экзаменов'
        unique_together = ['application', 'exam']


class News(models.Model):
    title = models.CharField(max_length=300, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='URL-идентификатор')
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to='news/%Y/%m/', blank=True, verbose_name='Изображение')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Автор')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']


class FAQ(models.Model):
    question = models.CharField(max_length=500, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ['order', 'id']


class Contact(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя контакта')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    address = models.TextField(blank=True, verbose_name='Адрес')
    office_hours = models.CharField(max_length=200, blank=True, verbose_name='Часы работы')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class DocumentTemplate(models.Model):
    FORMAT_CHOICES = [
        ('docx', 'Microsoft Word'),
        ('xlsx', 'Microsoft Excel'),
        ('pdf', 'PDF'),
    ]
    name = models.CharField(max_length=200, verbose_name='Название шаблона')
    file = models.FileField(upload_to='templates/', verbose_name='Файл шаблона')
    doc_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, verbose_name='Формат')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Шаблон документа'
        verbose_name_plural = 'Шаблоны документов'
        ordering = ['name']
