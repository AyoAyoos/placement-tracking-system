import os
import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "placement_system_Mvp.settings")
django.setup()

from tracker.models import Student, Company, Placement, Internship


def import_students():
    print("Importing Students...")
    df = pd.read_csv("Data/Student.csv")

    for _, row in df.iterrows():
        Student.objects.update_or_create(
            enrollment_no=row["enrollment_no"],
            defaults={
                "roll_no": str(row["roll_no"]),
                "full_name": row["full_name"],
                "email": row["email"],
                "contact_no": str(row["contact_no"]),
                "batch": str(row["batch"]),
                "degree": row["degree"],
                "department": row["department"],
                "class_division": row["class_division"],
            },
        )


def import_companies():
    print("Importing Companies...")
    df = pd.read_csv("Data/Company.csv")

    for _, row in df.iterrows():
        Company.objects.update_or_create(
            id=int(row["id"]),
            defaults={
                "name": row["name"],
                "city": row["city"],
                "domain": row["domain"],
                "contact_email": row["contact_email"],
                "contact_phone": str(row["contact_phone"]),
            },
        )


def import_placements():
    print("Importing Placements...")
    df = pd.read_csv("Data/Placement.csv")

    for _, row in df.iterrows():
        try:
            student = Student.objects.get(
                enrollment_no=row["student_enrollment"]
            )
            company = Company.objects.get(
                id=int(row["company_id"])
            )

            Placement.objects.update_or_create(
                student=student,
                company=company,
                defaults={
                    "ctc_lpa": float(row["ctc_lpa"]),
                    "role": row["role"],
                    "month_of_offer": row["month_of_offer"],
                },
            )

        except Student.DoesNotExist:
            print(f"Student not found: {row['student_enrollment']}")
        except Company.DoesNotExist:
            print(f"Company not found: {row['company_id']}")


def _parse_stipend(raw_value):
    """Split a CSV stipend cell ('15000' or 'Unpaid') into (is_paid, stipend_amount)."""
    raw = str(raw_value).strip()
    if raw.lower() == "unpaid":
        return False, None
    try:
        return True, int(float(raw))
    except (ValueError, TypeError):
        print(f"  Could not parse stipend value '{raw_value}', leaving amount blank")
        return True, None


def import_internships():
    print("Importing Internships...")
    df = pd.read_csv("Data/Internship.csv")

    for _, row in df.iterrows():
        try:
            student = Student.objects.get(
                enrollment_no=row["student_enrollment"]
            )
            company = Company.objects.get(
                id=int(row["company_id"])
            )

            is_paid, stipend_amount = _parse_stipend(row["stipend_monthly"])

            Internship.objects.update_or_create(
                student=student,
                company=company,
                defaults={
                    "source": row["source"],
                    "duration_months": str(row["duration_months"]),
                    "start_date": row["start_date"],
                    "end_date": row["end_date"],
                    "mode": row["mode"],
                    "is_paid": is_paid,
                    "stipend_amount": stipend_amount,
                },
            )

        except Student.DoesNotExist:
            print(f"Student not found: {row['student_enrollment']}")
        except Company.DoesNotExist:
            print(f"Company not found: {row['company_id']}")


if __name__ == "__main__":
    import_students()
    import_companies()
    import_placements()
    import_internships()
    print("✅ Data Imported Successfully!")