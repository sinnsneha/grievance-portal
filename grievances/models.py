from django.conf import settings
from django.db import models
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_sensitive = models.BooleanField(
        default=False,
        help_text="Sensitive categories go straight to the Super Admin.",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class BannedWord(models.Model):
    class Severity(models.IntegerChoices):
        MILD = 1, "Mild"
        SEVERE = 2, "Severe"

    word = models.CharField(max_length=50, unique=True)
    severity = models.IntegerField(choices=Severity.choices, default=Severity.MILD)

    class Meta:
        ordering = ["word"]

    def __str__(self):
        return self.word


class Submission(models.Model):
    class Kind(models.TextChoices):
        GRIEVANCE = "grievance", "Grievance"
        SUGGESTION = "suggestion", "Suggestion"

    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        ACKNOWLEDGED = "acknowledged", "Acknowledged"
        IN_PROGRESS = "in_progress", "In progress"
        RESOLVED = "resolved", "Resolved"
        REJECTED = "rejected", "Rejected"
        WITHDRAWN = "withdrawn", "Withdrawn"

    class Moderation(models.TextChoices):
        CLEAN = "clean", "Clean"
        FLAGGED = "flagged", "Flagged"
        CLEARED = "cleared", "Cleared"
        VIOLATION = "violation", "Violation"
        ESCALATED = "escalated", "Escalated"

    class Sentiment(models.TextChoices):
        POSITIVE = "positive", "Positive"
        NEUTRAL = "neutral", "Neutral"
        NEGATIVE = "negative", "Negative"

    kind = models.CharField(max_length=10, choices=Kind.choices)
    title = models.CharField(max_length=150)
    body = models.TextField()

    # One-to-many: a department and a category each have many submissions
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="submissions")
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="submissions")

    about_department_head = models.BooleanField(default=False)
    for_super_admin = models.BooleanField(default=False)

    status = models.CharField(max_length=15, choices=Status.choices, default=Status.SUBMITTED)
    status_reason = models.TextField(blank=True)
    moderation = models.CharField(max_length=10, choices=Moderation.choices, default=Moderation.CLEAN)

    sentiment = models.CharField(max_length=10, choices=Sentiment.choices, blank=True)
    sentiment_score = models.FloatField(null=True, blank=True)

    # Only the SHA-256 hash of the tracking code, never the code itself
    tracking_hash = models.CharField(max_length=64, unique=True, editable=False)
    caution_version = models.PositiveSmallIntegerField(default=1)

    # Dates only, never times (privacy rule)
    submitted_on = models.DateField(default=timezone.localdate)
    due_on = models.DateField(null=True, blank=True)
    closed_on = models.DateField(null=True, blank=True)

    # Many-to-many: a submission has several tags, a tag is on many submissions
    tags = models.ManyToManyField(Tag, blank=True, related_name="submissions")

    class Meta:
        ordering = ["-submitted_on", "-id"]

    def __str__(self):
        return f"#{self.pk} {self.title}"


class Message(models.Model):
    class Sender(models.TextChoices):
        STUDENT = "student", "Student"
        STAFF = "staff", "Staff"

    # One-to-many: one submission, a thread of many messages
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=10, choices=Sender.choices)
    staff_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    body = models.TextField()
    sent_on = models.DateField(default=timezone.localdate)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.get_sender_display()} on #{self.submission_id}"


class AuditLog(models.Model):
    """Staff actions only. Never logs a student submitting."""

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="audit_entries",
    )
    submission = models.ForeignKey(
        Submission,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_entries",
    )
    action = models.CharField(max_length=50)
    detail = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.created_at:%d %b %Y %H:%M} {self.action}"