import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Group, Student, Teacher, Subject, Grade

# Database connection
DATABASE_URL = "postgresql://postgres:123456@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def create_record(model, **kwargs):
    """Create a new record in the specified model."""
    record = model(**kwargs)
    session.add(record)
    session.commit()
    print(f"Created {model.__name__}: {kwargs}")


def list_records(model):
    """List all records in the specified model."""
    records = session.query(model).all()
    for record in records:
        print(record.__dict__)


def update_record(model, record_id, **kwargs):
    """Update a record in the specified model by ID."""
    record = session.query(model).filter_by(id=record_id).first()
    if record:
        for key, value in kwargs.items():
            setattr(record, key, value)
        session.commit()
        print(f"Updated {model.__name__} with ID {record_id}: {kwargs}")
    else:
        print(f"{model.__name__} with ID {record_id} not found.")


def delete_record(model, record_id):
    """Delete a record in the specified model by ID."""
    record = session.query(model).filter_by(id=record_id).first()
    if record:
        session.delete(record)
        session.commit()
        print(f"Deleted {model.__name__} with ID {record_id}")
    else:
        print(f"{model.__name__} with ID {record_id} not found.")


def main():
    parser = argparse.ArgumentParser(
        description="CLI for CRUD operations on the database."
    )
    parser.add_argument(
        "-a",
        "--action",
        required=True,
        choices=["create", "list", "update", "remove"],
        help="Action to perform",
    )
    parser.add_argument(
        "-m",
        "--model",
        required=True,
        choices=["Group", "Student", "Teacher", "Subject", "Grade"],
        help="Model to operate on",
    )
    parser.add_argument("--id", type=int, help="ID of the record (for update/remove)")
    parser.add_argument("--name", help="Name of the record (for create/update)")
    parser.add_argument("--group_id", type=int, help="Group ID (for Student)")
    parser.add_argument("--teacher_id", type=int, help="Teacher ID (for Subject)")
    parser.add_argument("--student_id", type=int, help="Student ID (for Grade)")
    parser.add_argument("--subject_id", type=int, help="Subject ID (for Grade)")
    parser.add_argument("--grade", type=float, help="Grade value (for Grade)")

    args = parser.parse_args()

    # Map model names to classes
    models = {
        "Group": Group,
        "Student": Student,
        "Teacher": Teacher,
        "Subject": Subject,
        "Grade": Grade,
    }
    model = models[args.model]

    if args.action == "create":
        kwargs = {}
        if args.name:
            kwargs["name"] = args.name
        if args.group_id:
            kwargs["group_id"] = args.group_id
        if args.teacher_id:
            kwargs["teacher_id"] = args.teacher_id
        if args.student_id:
            kwargs["student_id"] = args.student_id
        if args.subject_id:
            kwargs["subject_id"] = args.subject_id
        if args.grade:
            kwargs["grade"] = args.grade
        create_record(model, **kwargs)

    elif args.action == "list":
        list_records(model)

    elif args.action == "update":
        if not args.id:
            print("Error: --id is required for update action.")
            return
        kwargs = {}
        if args.name:
            kwargs["name"] = args.name
        if args.group_id:
            kwargs["group_id"] = args.group_id
        if args.teacher_id:
            kwargs["teacher_id"] = args.teacher_id
        if args.student_id:
            kwargs["student_id"] = args.student_id
        if args.subject_id:
            kwargs["subject_id"] = args.subject_id
        if args.grade:
            kwargs["grade"] = args.grade
        update_record(model, args.id, **kwargs)

    elif args.action == "remove":
        if not args.id:
            print("Error: --id is required for remove action.")
            return
        delete_record(model, args.id)


if __name__ == "__main__":
    main()
