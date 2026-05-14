-- PostgreSQL schema artifact for the Enrollsys project.
-- The live application continues to use DATABASES from app/settings.py.

CREATE TABLE IF NOT EXISTS core_faculty (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    short_name VARCHAR(50) NOT NULL DEFAULT '',
    description TEXT NOT NULL DEFAULT '',
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS core_department (
    id BIGSERIAL PRIMARY KEY,
    faculty_id BIGINT NOT NULL REFERENCES core_faculty(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    short_name VARCHAR(50) NOT NULL DEFAULT '',
    description TEXT NOT NULL DEFAULT '',
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS core_studyprogram (
    id BIGSERIAL PRIMARY KEY,
    department_id BIGINT NOT NULL REFERENCES core_department(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(20) NOT NULL,
    level VARCHAR(20) NOT NULL,
    form VARCHAR(20) NOT NULL,
    budget_places INTEGER NOT NULL DEFAULT 0,
    paid_places INTEGER NOT NULL DEFAULT 0,
    description TEXT NOT NULL DEFAULT '',
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS core_admissioncampaign (
    id BIGSERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'planned',
    description TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS core_userprofile (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES auth_user(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL DEFAULT 'applicant',
    phone VARCHAR(20) NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS core_application (
    id BIGSERIAL PRIMARY KEY,
    applicant_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    campaign_id BIGINT NOT NULL REFERENCES core_admissioncampaign(id) ON DELETE CASCADE,
    program_id BIGINT NOT NULL REFERENCES core_studyprogram(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    comment TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS core_applicationdocument (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT NOT NULL REFERENCES core_application(id) ON DELETE CASCADE,
    doc_type VARCHAR(20) NOT NULL,
    file VARCHAR(100) NOT NULL,
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    is_verified BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS core_exam (
    id BIGSERIAL PRIMARY KEY,
    program_id BIGINT NOT NULL REFERENCES core_studyprogram(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    exam_type VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    location VARCHAR(200) NOT NULL DEFAULT '',
    max_score INTEGER NOT NULL DEFAULT 100,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS core_examresult (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT NOT NULL REFERENCES core_application(id) ON DELETE CASCADE,
    exam_id BIGINT NOT NULL REFERENCES core_exam(id) ON DELETE CASCADE,
    score INTEGER NOT NULL,
    notes TEXT NOT NULL DEFAULT '',
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    recorded_by_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL,
    UNIQUE(application_id, exam_id)
);

CREATE TABLE IF NOT EXISTS core_news (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(300) NOT NULL,
    slug VARCHAR(50) NOT NULL UNIQUE,
    content TEXT NOT NULL,
    image VARCHAR(100) NOT NULL DEFAULT '',
    is_published BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    author_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS core_faq (
    id BIGSERIAL PRIMARY KEY,
    question VARCHAR(500) NOT NULL,
    answer TEXT NOT NULL,
    "order" INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS core_contact (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(254) NOT NULL,
    phone VARCHAR(20) NOT NULL DEFAULT '',
    address TEXT NOT NULL DEFAULT '',
    office_hours VARCHAR(200) NOT NULL DEFAULT '',
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS core_documenttemplate (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    file VARCHAR(100) NOT NULL,
    doc_format VARCHAR(10) NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);
