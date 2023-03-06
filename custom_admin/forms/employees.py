"""
This is file where the django documentation recommends you place all
your forms code, to keep your code easily maintainable.
"""

from django import forms

from employee.models import Employee

# -----------------------------------------------------------------------------
# Employee Forms
# -----------------------------------------------------------------------------


class MyEmployeeCreationForm(forms.ModelForm):
    """employee create"""

    class Meta:
        model = Employee
        fields = ["name", "employee_id", "address", "phone_number", "department", "working","is_active"]
    
    def save(self, commit=True):
        """
        save method to new employee storing it into the database.
        """
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance


class EmployeeChangeForm(forms.ModelForm):

    """Custom form to change employee"""

    class Meta:
        model = Employee
        fields = [
            "name",
            "employee_id",
            "address",
            "phone_number",
            "working",
            "department",
            "is_active",
        ]
