"""
Script for querying the database.

This script contains functions to perform various queries on the database,
such as finding top students, average grades, and subject assignments.
"""

from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Subject, Teacher, Grade

# Database connection
DATABASE_URL = "postgresql://postgres:yourpassword@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    """Find 5 students with the highest average grade across all subjects."""
    result = (
        session.query(Student.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade)
        .group_by(Student.id, Student.name)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )
    return result

def select_2(subject_name):
    """Find the student with the highest average grade in a specific subject."""
    result = (
        session.query(Student.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student.id, Student.name)
        .order_by(desc("avg_grade"))
        .first()
    )
    return result

def select_3(subject_name):
    """Find the average grade in groups for a specific subject."""
    result = (
        session.query(Group.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Student)
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Group.id, Group.name)
        .all()
    )
    return result

def select_4():
    """Find the average grade across all grades."""
    result = session.query(func.avg(Grade.grade).label("avg_grade")).scalar()
    return result

def select_5(teacher_name):
    """Find the subjects taught by a specific teacher."""
    result = (
        session.query(Subject.name)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .all()
    )
    return [row[0] for row in result]

def select_6(group_name):
    """Find the list of students in a specific group."""
    result = (
        session.query(Student.name)
        .join(Group)
        .filter(Group.name == group_name)
        .all()
    )
    return [row[0] for row in result]

def select_7(group_name, subject_name):
    """Find the grades of students in a specific group for a specific subject."""
    result = (
        session.query(Student.name, Grade.grade)
        .join(Grade)
        .join(Subject)
        .join(Group)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )
    return result

def select_8(teacher_name):
    """Find the average grade given by a specific teacher for their subjects."""
    result = (
        session.query(func.avg(Grade.grade).label("avg_grade"))
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .scalar()
    )
    return result

def select_9(student_name):
    """Find the list of subjects attended by a specific student."""
    result = (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .filter(Student.name == student_name)
        .distinct()
        .all()
    )
    return [row[0] for row in result]

def select_10(student_name, teacher_name):
    """Find the list of subjects that a specific teacher teaches to a specific student."""
    result = (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .join(Teacher)
        .filter(Student.name == student_name, Teacher.name == teacher_name)
        .distinct()
        .all()
    )
    return [row[0] for row in result]

def select_11(teacher_name, student_name):
    """Find the average grade that a specific teacher gives to a specific student."""
    result = (
        session.query(func.avg(Grade.grade).label("avg_grade"))
        .join(Subject)
        .join(Teacher)
        .join(Student)
        .filter(Teacher.name == teacher_name, Student.name == student_name)
        .scalar()
    )
    return result

def select_12(group_name, subject_name):
    """Find the grades of students in a specific group for a specific subject on the last lesson."""
    # First, find the latest date for the subject in the group
    latest_date = (
        session.query(func.max(Grade.date_received))
        .join(Student)
        .join(Group)
        .join(Subject)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .scalar()
    )

    # Then, get the grades for that date
    result = (
        session.query(Student.name, Grade.grade)
        .join(Grade)
        .join(Subject)
        .join(Group)
        .filter(
            Group.name == group_name,
            Subject.name == subject_name,
            Grade.date_received == latest_date
        )
        .all()
    )
    return result

# Example usage
if __name__ == "__main__":
    print("Select 1:", select_1())
    print("Select 2 (Math Studies):", select_2("Math Studies"))
    print("Select 3 (Math Studies):", select_3("Math Studies"))
    print("Select 4:", select_4())
    print("Select 5 (teacher name):", select_5("John Doe"))  # Replace with a teacher name
    print("Select 6 (Group-1):", select_6("Group-1"))
    print("Select 7 (Group-1, Math Studies):", select_7("Group-1", "Math Studies"))
    print("Select 8 (teacher name):", select_8("John Doe"))  # Replace with a teacher name
    print("Select 9 (student name):", select_9("Jane Doe"))  # Replace with a student name
    print("Select 10 (student name, teacher name):", select_10("Jane Doe", "John Doe"))
    print("Select 11 (teacher name, student name):", select_11("John Doe", "Jane Doe"))
    print("Select 12 (Group-1, Math Studies):", select_12("Group-1", "Math Studies"))
