import uuid

from django.db import models
from dataclasses import dataclass, field
from django.contrib.auth.models import AbstractUser, UserManager

from employee.models import ActivityTracking

# Create your models here.
@dataclass(frozen=True)
class UserID:
    """
    This is a value object that should be used to generate and pass the UserID to the UserFactory
    """

    id: uuid.UUID = field(init=False, default_factory=uuid.uuid4)


class UserManagerAutoID(UserManager):
    """
    A User Manager that sets the uuid on a model when calling the create_superuser function.
    """

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        if id not in extra_fields:
            extra_fields = dict(extra_fields, id=UserID().id)

        return self._create_user(username, email, password, **extra_fields)


# ----------------------------------------------------------------------
# User Model
# ----------------------------------------------------------------------


class User(AbstractUser, ActivityTracking):
    """
    A User replaces django's default user id with a UUID that should be created by the application, not the database.
    """

    STATUS_PENDING = "pending"
    STATUS_VERIFIED = "verified"
    STATUS_CHOICES = [
        (STATUS_PENDING, "pending"),
        (STATUS_VERIFIED, "verified"),
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(unique=True, blank=False, null=False)
    profile_image = models.ImageField(
        upload_to="images/", null=True, blank=True, verbose_name="profile_images"
    )
    google_auth_id = models.CharField(max_length=50, null=True, blank=True)
    is_new_user = models.BooleanField(default=True)
    is_verified = models.CharField(
        max_length=150, choices=STATUS_CHOICES, null=True, blank=True
    )

    objects = UserManagerAutoID()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "user"
