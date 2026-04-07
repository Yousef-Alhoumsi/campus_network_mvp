from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models


class BardEmailUserManager(UserManager):
    """Reject user creation when email is not in bard.edu domain."""

    def _normalize_and_validate_email(self, email):
        if not email:
            raise ValueError("An email address is required.")

        normalized_email = self.normalize_email(email)
        if not normalized_email.lower().endswith("@bard.edu"):
            raise ValueError("Email must end with @bard.edu.")
        return normalized_email

    def create_user(self, username, email=None, password=None, **extra_fields):
        email = self._normalize_and_validate_email(email)
        return super().create_user(
            username=username,
            email=email,
            password=password,
            **extra_fields,
        )

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        email = self._normalize_and_validate_email(email)
        return super().create_superuser(
            username=username,
            email=email,
            password=password,
            **extra_fields,
        )


class User(AbstractUser):
    email = models.EmailField(unique=True)

    objects = BardEmailUserManager()

    def clean(self):
        super().clean()
        if self.email and not self.email.lower().endswith("@bard.edu"):
            raise ValidationError({"email": "Email must end with @bard.edu."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
