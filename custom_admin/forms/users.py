"""
This is file where the django documentation recommends you place all
your forms code, to keep your code easily maintainable.
"""

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from custom_admin.utils.core import filter_perms
from user.models import User
from django.contrib.auth import get_user_model

# -----------------------------------------------------------------------------
# User Forms
# -----------------------------------------------------------------------------


class MyUserCreationForm(UserCreationForm):

    """Custom UserCreationForm."""

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta(UserCreationForm.Meta):
        """Define form properties here like model, fields, widgets, labels etc."""

        model = User
        fields = [
            "email",
            "username",
            "is_new_user",
            "first_name",
            "last_name",
            "profile_image",
            "password1",
            "password2",
            "is_verified",
            "is_active",
            "is_superuser",
        ]

    def __init__(self, user, *args, **kwargs):
        """This method works as a constructor"""
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        """
        Override this save method to add some extra functionality
        before actually storing it into the database.
        """
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance


class UserChangeForm(UserChangeForm, UserCreationForm):
    """Custom form to change User"""

    profile_image = forms.ImageField(widget=forms.FileInput, required=False)

    class Meta(UserChangeForm.Meta):
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "is_verified",
            "is_new_user",
            "is_active",
            "is_superuser",
        ]

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "attrs": "readonly"}
        )
        self.fields["password"].widget.attrs.update({"class": "form-control"})

    def clean(self):
        cleaned_data = super(UserChangeForm, self).clean()
        email = cleaned_data.get("email").strip().lower()

        full_name = cleaned_data.get("first_name")
        if not email:
            raise forms.ValidationError("Please add email.")
        if not full_name:
            raise forms.ValidationError("Please add name.")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.email = instance.email.strip().lower()
        if commit:
            instance.save()

        return instance
