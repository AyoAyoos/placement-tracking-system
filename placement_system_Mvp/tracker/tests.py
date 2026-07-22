from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import Company, Internship, Placement, Student


class CompanyModelTests(TestCase):
    def test_str_returns_name(self):
        company = Company.objects.create(name="Infosys", city="Hyderabad")
        self.assertEqual(str(company), "Infosys")

    def test_created_at_is_set_automatically(self):
        company = Company.objects.create(name="TCS")
        self.assertIsNotNone(company.created_at)
        self.assertIsNotNone(company.updated_at)


class StudentModelTests(TestCase):
    def test_str_includes_enrollment_and_name(self):
        student = Student.objects.create(
            enrollment_no="MITU22BTCS0001",
            full_name="Aarav Sharma",
            email="aarav@example.com",
            contact_no="9876543201",
            batch="2026",
        )
        self.assertIn("MITU22BTCS0001", str(student))
        self.assertIn("Aarav Sharma", str(student))


class PlacementModelTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            enrollment_no="MITU22BTCS0001",
            full_name="Aarav Sharma",
            email="aarav@example.com",
            contact_no="9876543201",
            batch="2026",
        )
        self.company = Company.objects.create(name="Infosys")

    def test_negative_ctc_fails_validation(self):
        placement = Placement(
            student=self.student,
            company=self.company,
            ctc_lpa=-5.0,
            role="ML Engineer",
            month_of_offer="October 2025",
        )
        with self.assertRaises(ValidationError):
            placement.full_clean()

    def test_duplicate_placement_for_same_student_company_is_rejected(self):
        Placement.objects.create(
            student=self.student, company=self.company,
            ctc_lpa=5.7, role="ML Engineer", month_of_offer="October 2025",
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Placement.objects.create(
                    student=self.student, company=self.company,
                    ctc_lpa=6.0, role="Backend Developer", month_of_offer="November 2025",
                )


class InternshipModelTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            enrollment_no="MITU22BTCS0002",
            full_name="Diya Patel",
            email="diya@example.com",
            contact_no="9876543202",
            batch="2026",
        )
        self.company = Company.objects.create(name="TCS")

    def test_unpaid_internship_has_no_stipend_amount(self):
        internship = Internship.objects.create(
            student=self.student, company=self.company,
            source="Referral", duration_months="3", mode="Remote",
            is_paid=False, stipend_amount=None,
        )
        self.assertFalse(internship.is_paid)
        self.assertIsNone(internship.stipend_amount)

    def test_duplicate_internship_for_same_student_company_is_rejected(self):
        Internship.objects.create(
            student=self.student, company=self.company,
            source="Referral", duration_months="3", mode="Remote",
            is_paid=True, stipend_amount=15000,
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Internship.objects.create(
                    student=self.student, company=self.company,
                    source="LinkedIn", duration_months="2", mode="Work from Office",
                    is_paid=True, stipend_amount=20000,
                )