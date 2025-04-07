"""
Script to seed the database with random data.

This script populates the database with groups, teachers, subjects, students,
and grades using the Faker library for generating realistic data.
"""

# Standard library imports
import random

# Third-party imports
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Local application imports
from models import Group, Student, Teacher, Subject, Grade

# Database connection configuration
DATABASE_URL = "postgresql://postgres:123456@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Initialize Faker for generating random data
fake = Faker()

# Create groups (3 groups)
groups = [Group(name=f"Group-{i+1}") for i in range(3)]
session.add_all(groups)
session.commit()

# Create teachers (5 teachers)
teachers = [Teacher(name=fake.name()) for _ in range(5)]
session.add_all(teachers)
session.commit()

# Create subjects (5-8 subjects, each assigned to a random teacher)
subjects = []
for i in range(random.randint(5, 8)):
    subject = Subject(
        name=fake.word().capitalize() + " Studies",
        teacher_id=random.choice(teachers).id,
    )
    subjects.append(subject)
session.add_all(subjects)
session.commit()

# Create students (30-50 students, each assigned to a random group)
students = []
for _ in range(random.randint(30, 50)):
    student = Student(
        name=fake.name(),
        group_id=random.choice(groups).id,
    )
    students.append(student)
session.add_all(students)
session.commit()

# Create grades (10-20 grades per student for random subjects)
for student in students:
    for _ in range(random.randint(10, 20)):
        grade = Grade(
            student_id=student.id,
            subject_id=random.choice(subjects).id,
            grade=round(random.uniform(2.0, 5.0), 1),  # Grades between 2.0 and 5.0
            date_received=fake.date_time_between(start_date="-1y", end_date="now"),
        )
        session.add(grade)
session.commit()

# Print confirmation message and close the session
print("Database seeded successfully!")
session.close()
