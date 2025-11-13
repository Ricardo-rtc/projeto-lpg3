from fastapi import APIRouter
from app.api.v1 import (
    auth, users, students, teachers, disciplines, 
    periods, classes, enrollments, assessments, grades, reports
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(teachers.router, prefix="/teachers", tags=["teachers"])
api_router.include_router(disciplines.router, prefix="/disciplines", tags=["disciplines"])
api_router.include_router(periods.router, prefix="/periods", tags=["periods"])
api_router.include_router(classes.router, prefix="/classes", tags=["classes"])
api_router.include_router(enrollments.router, prefix="/enrollments", tags=["enrollments"])
api_router.include_router(assessments.router, prefix="/assessments", tags=["assessments"])
api_router.include_router(grades.router, prefix="/grades", tags=["grades"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
