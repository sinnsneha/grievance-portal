from django.contrib import admin

from .models import StaffProfile


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "department"]
    list_filter = ["role", "department"]