from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from decimal import Decimal
import uuid
from app.models import Student, Enrollment, Grade, Assessment, Class, Discipline, Period, User
from app.schemas.report import StudentGradeReport, DisciplinePerformanceReport, PeriodReport

class ReportService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_student_grades_report(self, student_id: uuid.UUID) -> List[StudentGradeReport]:
        """Relatório de notas por aluno"""
        enrollments = self.db.query(Enrollment).join(Class).join(Discipline).join(Student).join(User)\
            .filter(Student.id == student_id).all()
        
        reports = []
        for enrollment in enrollments:
            grades_data = []
            for grade in enrollment.grades:
                grades_data.append({
                    'assessment_name': grade.assessment.name,
                    'score': float(grade.score),
                    'max_score': float(grade.assessment.max_score),
                    'weight': float(grade.assessment.weight),
                    'date': grade.assessment.date.isoformat() if grade.assessment.date else None
                })
            
            report = StudentGradeReport(
                student_id=student_id,
                student_name=enrollment.student.user.full_name or enrollment.student.user.username,
                registration_number=enrollment.student.registration_number,
                class_code=enrollment.class_.code,
                discipline_name=enrollment.class_.discipline.name,
                assessments=grades_data,
                final_average=enrollment.final_average,
                status=enrollment.status.value
            )
            reports.append(report)
        
        return reports
    
    def get_discipline_performance_report(self, discipline_id: uuid.UUID, period_id: uuid.UUID) -> DisciplinePerformanceReport:
        """Relatório de desempenho por disciplina"""
        classes = self.db.query(Class).filter(
            Class.discipline_id == discipline_id,
            Class.period_id == period_id
        ).all()
        
        total_students = 0
        sum_averages = Decimal(0)
        approved_students = 0
        
        for class_obj in classes:
            for enrollment in class_obj.enrollments:
                total_students += 1
                if enrollment.final_average:
                    sum_averages += enrollment.final_average
                    if enrollment.final_average >= 70:  # Média de aprovação
                        approved_students += 1
        
        average_grade = sum_averages / total_students if total_students > 0 else None
        approval_rate = (Decimal(approved_students) / Decimal(total_students) * 100) if total_students > 0 else None
        
        discipline = self.db.query(Discipline).filter(Discipline.id == discipline_id).first()
        period = self.db.query(Period).filter(Period.id == period_id).first()
        
        return DisciplinePerformanceReport(
            discipline_id=discipline_id,
            discipline_name=discipline.name if discipline else "",
            period_name=period.name if period else "",
            total_students=total_students,
            average_grade=average_grade,
            approval_rate=approval_rate
        )
    
    def get_period_report(self, period_id: uuid.UUID) -> PeriodReport:
        """Relatório geral do período"""
        period = self.db.query(Period).filter(Period.id == period_id).first()
        
        total_classes = self.db.query(func.count(Class.id))\
            .filter(Class.period_id == period_id).scalar()
        
        total_students = self.db.query(func.count(Enrollment.id.distinct()))\
            .join(Class).filter(Class.period_id == period_id).scalar()
        
        total_disciplines = self.db.query(func.count(Discipline.id.distinct()))\
            .join(Class).filter(Class.period_id == period_id).scalar()
        
        return PeriodReport(
            period_id=period_id,
            period_name=period.name if period else "",
            start_date=period.start_date if period else None,
            end_date=period.end_date if period else None,
            total_classes=total_classes or 0,
            total_students=total_students or 0,
            total_disciplines=total_disciplines or 0
        )
