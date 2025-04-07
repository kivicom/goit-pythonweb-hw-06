"""
SQLAlchemy models for a student database.

This module defines the database schema for managing students, groups, teachers,
subjects, and grades, with relationships between them.
"""

# Standard library imports
from datetime import datetime

# Third-party imports
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship, declarative_base

# Initialize the SQLAlchemy Base class for model definitions
Base = declarative_base()


class Group(Base):
    """
    Model representing a group of students.

    Attributes:
        id (int): Primary key for the group.
        name (str): Unique name of the group.
        students (relationship): List of students in the group.
    """

    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    students = relationship("Student", back_populates="group")


class Student(Base):
    """
    Model representing a student.

    Attributes:
        id (int): Primary key for the student.
        name (str): Name of the student.
        group_id (int): Foreign key referencing the group.
        group (relationship): The group the student belongs to.
        grades (relationship): List of grades for the student.
    """

    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")


class Teacher(Base):
    """
    Model representing a teacher.

    Attributes:
        id (int): Primary key for the teacher.
        name (str): Name of the teacher.
        subjects (relationship): List of subjects taught by the teacher.
    """

    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    subjects = relationship("Subject", back_populates="teacher")


class Subject(Base):
    """
    Model representing a subject.

    Attributes:
        id (int): Primary key for the subject.
        name (str): Name of the subject.
        teacher_id (int): Foreign key referencing the teacher.
        teacher (relationship): The teacher who teaches the subject.
        grades (relationship): List of grades for the subject.
    """

    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")


class Grade(Base):
    """
    Model representing a grade for a student in a subject.

    Attributes:
        id (int): Primary key for the grade.
        student_id (int): Foreign key referencing the student.
        subject_id (int): Foreign key referencing the subject.
        grade (float): The grade value.
        date_received (datetime): The date when the grade was received.
        student (relationship): The student who received the grade.
        subject (relationship): The subject for which the grade was given.
    """

    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    grade = Column(Float, nullable=False)
    date_received = Column(DateTime, default=datetime.utcnow)
    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")
