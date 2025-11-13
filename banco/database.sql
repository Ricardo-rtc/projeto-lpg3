CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE DATABASE projetolpdb;

CREATE TYPE user_role AS ENUM ('student', 'teacher', 'admin');

CREATE TYPE enrollment_status AS ENUM (
    'matriculado',
    'trancado',
    'concluido',
    'cancelado'
);

CREATE TABLE
    users (
        id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role user_role NOT NULL DEFAULT 'student',
        full_name TEXT,
        created_at timestamptz NOT NULL DEFAULT now (),
        updated_at timestamptz NOT NULL DEFAULT now ()
    );

CREATE TABLE
    students (
        id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
        user_id uuid UNIQUE NOT NULL REFERENCES users (id) ON DELETE CASCADE,
        registration_number TEXT UNIQUE,
        enrollment_date date,
        birth_date date,
        active boolean NOT NULL DEFAULT true
    );

CREATE TABLE
    teachers (
        id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
        user_id uuid UNIQUE NOT NULL REFERENCES users (id) ON DELETE CASCADE,
        employee_number TEXT UNIQUE,
        hire_date date
    );

CREATE TABLE
    periods (
        id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
        code TEXT NOT NULL,
        name TEXT,
        start_date date,
        end_date date,
        active boolean DEFAULT true
    );

CREATE TABLE
    disciplines (
        id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        credits integer
    );

CREATE TABLE
    classes (
        id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
        discipline_id uuid NOT NULL REFERENCES disciplines (id) ON DELETE RESTRICT,
        period_id uuid NOT NULL REFERENCES periods (id) ON DELETE RESTRICT,
        teacher_id uuid REFERENCES teachers (id) ON DELETE SET NULL,
        code TEXT,
        capacity integer,
        created_at timestamptz DEFAULT now ()
    );

CREATE TABLE
    enrollments (
        id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
        student_id uuid NOT NULL REFERENCES students (id) ON DELETE CASCADE,
        class_id uuid NOT NULL REFERENCES classes (id) ON DELETE CASCADE,
        enrolled_at timestamptz DEFAULT now (),
        status enrollment_status NOT NULL DEFAULT 'matriculado',
        final_average numeric(5, 2),
        CONSTRAINT uq_enrollment UNIQUE (student_id, class_id)
    );

CREATE TABLE
    assessments (
        id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
        class_id uuid NOT NULL REFERENCES classes (id) ON DELETE CASCADE,
        name TEXT NOT NULL,
        description TEXT,
        date date,
        weight numeric(5, 2) NOT NULL DEFAULT 1.0,
        max_score numeric(8, 2) DEFAULT 100,
        created_at timestamptz DEFAULT now ()
    );

CREATE TABLE
    grades (
        id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
        enrollment_id uuid NOT NULL REFERENCES enrollments (id) ON DELETE CASCADE,
        assessment_id uuid NOT NULL REFERENCES assessments (id) ON DELETE CASCADE,
        score numeric(8, 2) NOT NULL CHECK (score >= 0),
        recorded_by uuid REFERENCES users (id),
        recorded_at timestamptz DEFAULT now (),
        CONSTRAINT uq_grade UNIQUE (enrollment_id, assessment_id)
    );

CREATE TABLE
    IF NOT EXISTS audit_logs (
        id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
        schema_name TEXT NOT NULL,
        table_name TEXT NOT NULL,
        operation TEXT NOT NULL,
        record_id TEXT,
        changed_data jsonb,
        changed_by TEXT DEFAULT current_user,
        changed_at timestamptz DEFAULT now ()
    );

CREATE TABLE
    permissions (
        id serial PRIMARY KEY,
        role user_role NOT NULL,
        resource TEXT NOT NULL,
        can_read bool DEFAULT false,
        can_write bool DEFAULT false,
        can_delete bool DEFAULT false
    );

CREATE INDEX idx_users_email ON users (email);

CREATE INDEX idx_students_registration ON students (registration_number);

CREATE INDEX idx_classes_period ON classes (period_id);

CREATE INDEX idx_enrollments_student ON enrollments (student_id);

CREATE INDEX idx_assessments_class ON assessments (class_id);

CREATE INDEX idx_grades_enrollment ON grades (enrollment_id);

CREATE OR REPLACE FUNCTION audit_all_tables()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  data jsonb;
  key_name TEXT;
  record_pk TEXT;
BEGIN
  IF (TG_OP = 'DELETE') THEN
    data := to_jsonb(OLD);
  ELSE
    data := to_jsonb(NEW);
  END IF;

  SELECT a.attname INTO key_name
  FROM pg_index i
  JOIN pg_attribute a ON a.attrelid = i.indrelid
                     AND a.attnum = ANY(i.indkey)
  WHERE i.indrelid = TG_RELID
    AND i.indisprimary
  LIMIT 1;

  IF key_name IS NOT NULL THEN
    IF TG_OP = 'DELETE' THEN
      record_pk := OLD.*::jsonb ->> key_name;
    ELSE
      record_pk := NEW.*::jsonb ->> key_name;
    END IF;
  ELSE
    record_pk := NULL;
  END IF;

  INSERT INTO audit_logs(schema_name, table_name, operation, record_id, changed_data)
  VALUES (TG_TABLE_SCHEMA, TG_TABLE_NAME, TG_OP, record_pk, data);

  RETURN NULL;
END;
$$;
