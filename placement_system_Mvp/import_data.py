import os
import django
import pandas as pd

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_system_Mvp.settings')
django.setup()

from tracker.models import Company, Student, Placement

def import_csv():
    # Import Companies
    df_comp = pd.read_csv('Data/companies.csv')
    for _, row in df_comp.iterrows():
        Company.objects.get_or_create(
            company_id=row['company_id'],
            company_name=row['company_name'],
            tier=row['tier']
        )

    # Import Students
    df_stud = pd.read_csv('Data/students.csv')
    for _, row in df_stud.iterrows():
        Student.objects.get_or_create(
            roll_no=row['roll_no'],
            name=row['name'],
            specialization=row['specialization'],
            cgpa=row['cgpa']
        )

    # Import Placements
    df_place = pd.read_csv('Data/placements.csv')
    for _, row in df_place.iterrows():
        student = Student.objects.get(roll_no=row['roll_no'])
        company = Company.objects.get(company_id=row['company_id'])
        Placement.objects.get_or_create(
            placement_id=row['placement_id'],
            student=student,
            company=company,
            package_lpa=row['package_lpa']
        )
    print("Data imported successfully!")

if __name__ == "__main__":
    import_csv()