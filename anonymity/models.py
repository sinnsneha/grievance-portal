from django.conf import settings
from django.db import models
from django.utils import timezone


class OTPChallenge(models.Model):
    """A pending OTP. Stored by pseudonym, never by email, and deleted once used."""

    pseudonym = models.CharField(max_length=64, db_index=True)
    code_hash = models.CharField(max_length=64)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)


class Offender(models.Model):
    """A pseudonym with at least one confirmed violation."""

    pseudonym = models.CharField(max_length=64, unique=True)
    blocked_until = models.DateField(null=True, blank=True)
    warning_pending = models.BooleanField(default=False)

    def alias(self):
        return f"Offender #{self.pseudonym[:4].upper()}"

    def __str__(self):
        return self.alias()


class Strike(models.Model):
    # One-to-many: an offender collects strikes
    offender = models.ForeignKey(Offender, on_delete=models.CASCADE, related_name="strikes")
    submission = models.ForeignKey(
        "grievances.Submission",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="strikes",
    )
    reason = models.CharField(max_length=200)
    given_on = models.DateField(default=timezone.localdate)

    class Meta:
        ordering = ["-given_on"]

    def __str__(self):
        return f"{self.offender} on {self.given_on}"


class ModerationCase(models.Model):
    """Exists only while a post is flagged or confirmed. Deleted if the post is cleared."""

    # One-to-one: a flagged submission has exactly one case
    submission = models.OneToOneField(
        "grievances.Submission",
        on_delete=models.CASCADE,
        related_name="moderation_case",
    )
    pseudonym = models.CharField(max_length=64)
    identity_lock = models.TextField()  # the email, encrypted with Fernet
    matched_words = models.CharField(max_length=200, blank=True)
    decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    revealed = models.BooleanField(default=False)

    def __str__(self):
        return f"Case for #{self.submission_id}"