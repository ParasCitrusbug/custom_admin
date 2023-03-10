import uuid

from django.db import models
from django.contrib.auth.hashers import make_password


class ActivityTracking(models.Model):
    """for Activity check user and employee data"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


DEPARTMENT_CHOICES = (
    ("Mechanical", "Mechanical"),
    ("Computer", "Computer"),
    ("IT", "IT"),
    ("Electrical", "Electrical"),
)


class Employee(ActivityTracking):
    """Employee data models"""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, auto_created=True
    )
    name = models.CharField(max_length=20)
    employee_id = models.CharField(max_length=15, unique=True)
    phone_number = models.PositiveIntegerField(unique=True)
    address = models.TextField()
    working = models.BooleanField(default=True)
    department = models.CharField(
        max_length=16, choices=DEPARTMENT_CHOICES, default=None
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        db_table = "employee"
