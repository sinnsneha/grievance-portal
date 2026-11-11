from django.contrib import admin

from .models import AuditLog, BannedWord, Category, Department, Message, Submission, Tag


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "is_active"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "is_sensitive"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(BannedWord)
class BannedWordAdmin(admin.ModelAdmin):
    list_display = ["word", "severity"]
    list_filter = ["severity"]
    search_fields = ["word"]


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "kind", "department", "status", "moderation", "submitted_on"]
    list_filter = ["kind", "status", "moderation", "department", "category"]
    search_fields = ["title", "body"]
    filter_horizontal = ["tags"]
    inlines = [MessageInline]

    def has_add_permission(self, request):
        # Submissions are only created through the student form (Section 5)
        return False


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["created_at", "actor", "action", "submission"]
    list_filter = ["action"]