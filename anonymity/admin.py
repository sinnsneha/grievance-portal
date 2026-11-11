from django.contrib import admin

from .models import ModerationCase, Offender, Strike


class StrikeInline(admin.TabularInline):
    model = Strike
    extra = 0


@admin.register(Offender)
class OffenderAdmin(admin.ModelAdmin):
    list_display = ["alias", "blocked_until", "warning_pending"]
    readonly_fields = ["pseudonym"]
    inlines = [StrikeInline]


@admin.register(ModerationCase)
class ModerationCaseAdmin(admin.ModelAdmin):
    list_display = ["submission", "revealed", "decided_by"]
    # The identity lock is never shown here. Revealing happens only
    # through the logged Reveal button we build in Section 7.
    exclude = ["identity_lock"]
    readonly_fields = ["pseudonym"]