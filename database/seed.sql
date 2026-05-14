-- Demo PostgreSQL seed artifact. It does not alter Django settings.

INSERT INTO core_faculty (id, name, short_name, description, is_active) VALUES
    (1, 'Факультет экономики и финансов', 'ФЭФ', 'Подготовка специалистов в области экономики, финансов и учета.', TRUE),
    (2, 'Факультет управления', 'ФУ', 'Направления по менеджменту, управлению персоналом и государственному управлению.', TRUE)
ON CONFLICT DO NOTHING;

INSERT INTO core_department (id, faculty_id, name, short_name, description, is_active) VALUES
    (1, 1, 'Кафедра экономики', 'КЭ', 'Экономика, финансы и аналитика.', TRUE),
    (2, 2, 'Кафедра менеджмента', 'КМ', 'Менеджмент и проектное управление.', TRUE)
ON CONFLICT DO NOTHING;

INSERT INTO core_studyprogram (id, department_id, name, code, level, form, budget_places, paid_places, description, is_active) VALUES
    (1, 1, 'Экономика', '38.03.01', 'bachelor', 'full_time', 15, 80, 'Профиль для будущих экономистов и финансовых аналитиков.', TRUE),
    (2, 2, 'Менеджмент', '38.03.02', 'bachelor', 'distance', 10, 100, 'Подготовка управленцев для бизнеса и государственных организаций.', TRUE)
ON CONFLICT DO NOTHING;

INSERT INTO core_admissioncampaign (id, year, start_date, end_date, status, description) VALUES
    (1, 2026, '2026-06-01', '2026-08-25', 'active', 'Основная приемная кампания 2026 года.')
ON CONFLICT DO NOTHING;

INSERT INTO core_faq (id, question, answer, "order", is_active) VALUES
    (1, 'Как подать заявление?', 'Создайте личный кабинет, выберите направление и отправьте заявку.', 1, TRUE),
    (2, 'Можно ли загрузить документы онлайн?', 'Да, документы прикрепляются к заявке в личном кабинете.', 2, TRUE)
ON CONFLICT DO NOTHING;

INSERT INTO core_contact (id, name, email, phone, address, office_hours, is_active) VALUES
    (1, 'Управление по организации приема', 'admission@muiv.ru', '+7 (495) 783-68-48', 'Москва, 2-й Кожуховский проезд, 12', 'Пн-Пт 10:00-18:00', TRUE)
ON CONFLICT DO NOTHING;

INSERT INTO core_news (id, title, slug, content, image, is_published, created_at, updated_at, author_id) VALUES
    (1, 'Открыт прием документов', 'opened-admission-2026', 'Абитуриенты могут подать заявление через личный кабинет.', '', TRUE, NOW(), NOW(), NULL)
ON CONFLICT DO NOTHING;
