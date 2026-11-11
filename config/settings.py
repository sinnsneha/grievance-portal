"""
Django settings for the Anonymous Grievance & Suggestion Portal.
Secret values are read from the .env file, never written here.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Project folder (the one that contains manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Load the secret values from .env
load_dotenv(BASE_DIR / ".env")


# ---------------------------------------------------------------
# Core settings
# ---------------------------------------------------------------

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = os.environ.get("DEBUG") == "True"

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# ---------------------------------------------------------------
# Apps
# ---------------------------------------------------------------

INSTALLED_APPS = [
    # Django's built-in apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Our apps
    "accounts",
    "anonymity",
    "grievances",
    "reports",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# ---------------------------------------------------------------
# Database
# ---------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ---------------------------------------------------------------
# Passwords (used for staff accounts)
# ---------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ---------------------------------------------------------------
# Language and time
# ---------------------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------
# Static files (CSS, JavaScript, Bootstrap)
# ---------------------------------------------------------------

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]


# ---------------------------------------------------------------
# Keys for anonymity (Section 1)
# ---------------------------------------------------------------

PSEUDONYM_KEY = os.environ["PSEUDONYM_KEY"]
IDENTITY_LOCK_KEY = os.environ["IDENTITY_LOCK_KEY"]


# ---------------------------------------------------------------
# Project rules (Section 1)
# ---------------------------------------------------------------

ALLOWED_EMAIL_DOMAIN = os.environ["ALLOWED_EMAIL_DOMAIN"]
CAUTION_VERSION = 1
STRIKES_TO_BLOCK = 3
STRIKE_WINDOW_DAYS = 120
BLOCK_DAYS = 30


# --------------------------------------------