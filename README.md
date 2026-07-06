Placement System (MVP)
Django-based placement and internship tracker for a Training & Placement (T&P) cell. Manages students, companies, placement offers, and internships. Data can be bulk-imported from CSV files aligned with the T&P Excel format.

Status: MVP — Django Admin is the primary UI. No public-facing views yet.

Tech Stack
Layer	Technology
Backend
Django 6.0.6
Database
SQLite (db.sqlite3)
Data import
pandas
Admin UI
Django Admin
Python dependencies: django, pandas (no requirements.txt in repo yet — install manually)

Project Structure
Placement_System/
├── README.md                          # This file
├── Sample-data-structure-TNP.xlsx     # Reference Excel format from T&P office
└── placement_system_Mvp/
    ├── manage.py                      # Django CLI entry point
    ├── import_data.py                 # Bulk CSV → database import script
    ├── db.sqlite3                     # SQLite DB (gitignored, created after migrate)
    ├── Data/                          # Sample CSV datasets
    │   ├── Student.csv
    │   ├── Company.csv
    │   ├── Placement.csv
    │   └── Internship.csv
    ├── placement_system_Mvp/          # Django project config
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    └── tracker/                       # Main Django app
        ├── models.py                  # Company, Student, Placement, Internship
        ├── admin.py                   # Admin registrations
        ├── views.py                   # Empty (future public views)
        ├── migrations/
        └── tests.py
Data Model
Four models in tracker/models.py:

Company (master)
    ├── Placement (FK → Student, Company)
    └── Internship (FK → Student, Company)
Student (master, PK = enrollment_no)
    ├── placements (related_name)
    └── internships (related_name)
Model	Purpose	Key fields
Company
Shared company master
name (unique), city, domain, contact_email, contact_phone
Student
Roll call list
enrollment_no (PK), roll_no, full_name, email, batch, department, class_division
Placement
Final placement offers
student, company, ctc_lpa, role, month_of_offer
Internship
Internship records
student, company, source, duration_months, start_date, end_date, mode, stipend_monthly, offer_letter
Models map to T&P Excel sheets:

Student → Roll Call List
Placement → Placement-Data-format
Internship → Internship data format
Company → Extracted from placement/internship sheets (deduplicated)
See Sample-data-structure-TNP.xlsx at the repo root for the official column layout.

Getting Started
Prerequisites
Python 3.10+
pip
1. Clone and enter the project
git clone <repository-url>
cd Placement_System/placement_system_Mvp
2. Create a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
3. Install dependencies
pip install django pandas
4. Apply database migrations
python manage.py migrate
5. Create an admin user
python manage.py createsuperuser
6. Run the development server
python manage.py runserver
Open http://127.0.0.1:8000/admin/ and log in with the superuser account.

Importing Sample Data
CSV files live in placement_system_Mvp/Data/. Import order matters: students and companies first, then placements and internships.

cd placement_system_Mvp
python import_data.py
The script uses update_or_create, so re-running it is safe. Missing student/company references are printed to the console and skipped.

CSV Column Reference
Student.csv

Column	Required	Example
enrollment_no
Yes (PK)
MITU22BTCS0001
roll_no
No
1
full_name
Yes
Aarav Sharma
email
Yes
aarav.sharma@mitu.edu.in
contact_no
Yes
9876543201
batch
Yes
2026
degree
Yes
B.Tech
department
No
AI & DS
class_division
No
LY AIA
Company.csv

Column	Required	Example
id
Yes
1
name
Yes
Infosys
city
No
Hyderabad
domain
No
Cybersecurity
contact_email
No
hr@infosys.com
contact_phone
No
02070000001
Placement.csv

Column	Required	Example
student_enrollment
Yes (FK)
MITU22BTCS0001
company_id
Yes (FK)
1
ctc_lpa
Yes
5.7
role
Yes
ML Engineer
month_of_offer
Yes
October 2025
Internship.csv

Column	Required	Example
student_enrollment
Yes (FK)
MITU22BTCS0001
company_id
Yes (FK)
1
source
Yes
LinkedIn
duration_months
Yes
2
start_date
No
2025-06-01
end_date
No
2025-08-31
mode
Yes
Remote
stipend_monthly
Yes
15000 or Unpaid
Django Admin
All four models are registered in tracker/admin.py with search and filters:

Companies — search by name/domain; filter by city
Students — search by enrollment, roll, name, email; filter by batch, division, department
Placements — search by student/company; filter by company and offer month
Internships — search by student/company; filter by mode, source, company
Internship offer_letter PDFs upload to offer_letters/ (configure MEDIA_ROOT / MEDIA_URL in settings before using file uploads in production).

Configuration Notes
Setting	Location	Default
Database
settings.py
SQLite at placement_system_Mvp/db.sqlite3
DEBUG
settings.py
True (dev only)
SECRET_KEY
settings.py
Insecure placeholder — change before production
URLs
urls.py
Only /admin/ is wired
tracker/views.py is a stub. Public dashboards or APIs are not implemented yet.

Common Commands
# New migration after model changes
python manage.py makemigrations
python manage.py migrate
# Django shell
python manage.py shell
# Run tests (placeholder)
python manage.py test tracker
Development Roadmap (not yet built)
Public or role-based UI (student / T&P officer)
REST API
Excel import (direct from Sample-data-structure-TNP.xlsx)
requirements.txt and environment-based settings
Production database (PostgreSQL) and media file storage
Reports and analytics (placement %, CTC stats, company-wise breakdown)
Gitignored Files
Per .gitignore: db.sqlite3, virtualenv folders, __pycache__/, .env, IDE and OS junk files.

License
Not specified. Confirm with the project owner before external use.

