from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class StaffProfile(models.Model):
    """A login's authority role and, for a Department Admin, their department."""

    class Role(models.TextChoices):
        DEPARTMENT_ADMIN = "department_admin", "Department Admin"
        SUPER_ADMIN = "super_admin", "Super Admin"

    # One-to-one: each authority login has exactly one profile
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_profile",
    )
    role = models.CharField(max_length=20, choices=Role.choices)
    department = models.ForeignKey(
        "grievances.Department",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="admins",
    )

    class Meta:
        verbose_name = "authority profile"
        verbose_name_plural = "authority profiles"

    def clean(self):
        if self.role == self.Role.DEPARTMENT_ADMIN and self.department is None:
            raise ValidationError({"department": "A Department Admin needs a department."})
        if self.role == self.Role.SUPER_ADMIN and self.department is not None:
            raise ValidationError({"department": "Leave this empty for the Super Admin."})

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"