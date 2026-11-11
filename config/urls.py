"""
Main URL list for the project.
Each app's pages get added here as we build them.
"""

from django.contrib import admin
from django.urls import path

urlpatterns = [
    # Django Admin, moved away from /admin/ so it isn't
    # confused with the staff dashboards we build later
    path("django-admin/", admin.site.urls),
]