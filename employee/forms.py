from django import forms

from employee import models


class EmployeeForm(forms.Form):
    """Employee data form"""

    class Meta:
        model = models.EmployeeData
        fields = "__all__"


class UserForm(forms.ModelForm):
    """User data form"""

    class Meta:
        model = models.UserData
        fields = ("email", "password")
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password": forms.TextInput(attrs={"class": "form-control"}),
        }


class ForgotPasswordForm(forms.ModelForm):
    """forgot password form"""

    class Meta:
        model = models.UserData
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class ChangePasswordForm(forms.Form):
    """Change password form"""

    new_password = forms.CharField(max_length=16)
    confirm_password = forms.CharField(max_length=16)

    new_password.widget.attrs = {"class": "form-control"}
    confirm_password.widget.attrs = {"class": "form-control"}
