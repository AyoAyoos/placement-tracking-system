from django.db import models

class Company(models.Model):
    # Using company_id exactly as it is in your CSV
    company_id = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=255)
    tier = models.CharField(max_length=50) # 'Dream' or 'Mass Recruiter'

    def __str__(self):
        return self.company_name
    
    class Meta:
        verbose_name_plural = "Companies"

class Student(models.Model):
    # ADT... numbers go here as the primary key
    roll_no = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=50)
    cgpa = models.FloatField()
    is_placed = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.roll_no} - {self.name}"

class Placement(models.Model):
    placement_id = models.IntegerField(primary_key=True)
    # Foreign Keys link the Placement to the specific Student and Company
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='placements')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    package_lpa = models.FloatField()

    def __str__(self):
        return f"{self.student.name} at {self.company.company_name} ({self.package_lpa} LPA)"
