from django.core.validators import MinValueValidator
from django.db import models


# 1. Company Master
# Extracted from both Placement and Internship sheets to avoid duplication.
class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)  # e.g., "Danfoss"
    city = models.CharField(max_length=100, blank=True, null=True)
    domain = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"


# 2. Student Master
# Maps directly to the "Roll Call List" Sheet
class Student(models.Model):
    enrollment_no = models.CharField(max_length=50, primary_key=True)  # e.g., MITU22BTCS0300
    roll_no = models.CharField(max_length=50, blank=True, null=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_no = models.CharField(max_length=20)
    batch = models.CharField(max_length=10)  # e.g., 2026
    degree = models.CharField(max_length=50, default="B.Tech.")
    department = models.CharField(max_length=100, blank=True, null=True)
    class_division = models.CharField(max_length=50, blank=True, null=True)  # e.g., LY AIA

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.enrollment_no} - {self.full_name}"


# 3. Placement Offers
# Maps directly to the "Placement-Data-format" Sheet
class Placement(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='placements')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    ctc_lpa = models.FloatField(
        help_text="CTC in Lakhs Per Annum",
        validators=[MinValueValidator(0.0)],
    )
    role = models.CharField(max_length=255)
    month_of_offer = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.student.full_name} placed at {self.company.name}"

    class Meta:
        # A student can only have one placement record per company.
        # Re-imports use update_or_create keyed on (student, company), so this
        # constraint keeps the DB consistent with that assumption at the DB level too.
        constraints = [
            models.UniqueConstraint(fields=['student', 'company'], name='unique_placement_per_student_company'),
        ]


# 4. Internships
# Maps directly to the "Internship data format" Sheet
class Internship(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='internships')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)  # e.g., Central T & P
    duration_months = models.CharField(max_length=50)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    mode = models.CharField(max_length=100)  # Work from Office / Remote

    # Replaces the old free-text `stipend_monthly` string field (which mixed
    # numbers with "Unpaid"). Split so charts/reports and Power BI can treat
    # stipend as a real number instead of parsing a string every time.
    is_paid = models.BooleanField(default=True)
    stipend_amount = models.PositiveIntegerField(
        blank=True, null=True,
        help_text="Monthly stipend in INR. Leave blank if unpaid.",
    )

    # Allows faculty to upload the actual PDF offer letters
    offer_letter = models.FileField(upload_to='offer_letters/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.company.name} Internship"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'company'], name='unique_internship_per_student_company'),
        ]