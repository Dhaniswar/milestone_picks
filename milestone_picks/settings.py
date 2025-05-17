from pathlib import Path
import os
import socket
from datetime import timedelta
from django.http import HttpResponseForbidden
import requests
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()


import requests

import logging

logger = logging.getLogger("django.security.DisallowedHost")



def skip_disallowed_hosts(get_response):
    def middleware(request):
        # Bypass host check for health endpoints
        if request.path in ['/health/', '/health']:
            return get_response(request)
            
        try:
            host = request.get_host()
            return get_response(request)
        except Exception as e:
            if "DisallowedHost" in str(e):
                host = request.META.get('HTTP_HOST', 'unknown')
                logger.warning(f"Blocked request with invalid host: {host}")
                return HttpResponseForbidden("Invalid host header")
            raise
    return middleware



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")






def get_ec2_instance_ips():
    """Get all possible EC2 instance IPs"""
    try:
        # Get private IP
        hostname = socket.gethostname()
        private_ip = socket.gethostbyname(hostname)
        
        # Get public IP if available
        try:
            public_ip = requests.get('http://169.254.169.254/latest/meta-data/public-ipv4', timeout=0.1).text
        except:
            public_ip = None
            
        return {private_ip, public_ip} if public_ip else {private_ip}
    except:
        return set()




# Set ALLOWED_HOSTS based on the environment
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# Dynamic host configuration
ALLOWED_HOSTS = [
    "52.4.219.148",
    "34.200.210.186",
    "milestone-picks.eba-y7t33j83.us-east-1.elasticbeanstalk.com",
    "api.milestonepicks.com",
    "milestonepicks.com",
    "www.milestonepicks.com",
    ".elasticbeanstalk.com",
    ".us-east-1.elasticbeanstalk.com",
    "localhost",
    "127.0.0.1",
    'iseewhere.com',
    'tableau-poc.q-centrix.com',
    'tridot.com',
    'webhooks.flightstats.com',
    '44.193.164.124',
    '52.45.25.47'
]

# Add EC2 instance IPs
ALLOWED_HOSTS.extend(get_ec2_instance_ips())


# Security settings
if DEBUG:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0
else:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True


CORS_ALLOW_ALL_ORIGINS = False

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://milestonepicks.com",
    "https://www.milestonepicks.com",
    "https://api.milestonepicks.com"
    
]


CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# If your frontend needs to send credentials (cookies, auth headers)
CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]


# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"


AUTH_USER_MODEL = "user.User"

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "rest_framework_swagger",
    "drf_yasg",
    "django_filters",
    "rest_framework_simplejwt",
    "storages",
    "user",
    "predictions",
    "subscriptions",
    "core",
    "bettinginfo",
    "aboutsection",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "milestone_picks.settings.skip_disallowed_hosts",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",  # Only authenticated users can access
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}


# Conditionally add the custom middleware in production
if not DEBUG:
    MIDDLEWARE.insert(0, "milestone_picks.settings.skip_disallowed_hosts")


# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
AWS_S3_CUSTOM_DOMAIN = f'{os.environ.get("AWS_STORAGE_BUCKET_NAME")}.s3.{os.environ.get("AWS_S3_REGION_NAME")}.amazonaws.com'

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"


# STORAGES configuration for both media and static files


ROOT_URLCONF = "milestone_picks.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "libraries": {
                "staticfiles": "django.templatetags.static",
            },
        },
    },
]

WSGI_APPLICATION = "milestone_picks.wsgi.application"


STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "access_key": os.environ.get("AWS_ACCESS_KEY_ID"),
            "secret_key": os.environ.get("AWS_SECRET_ACCESS_KEY"),
            "bucket_name": os.environ.get("AWS_STORAGE_BUCKET_NAME"),
            "region_name": os.environ.get("AWS_S3_REGION_NAME"),
            "custom_domain": f'{os.environ.get("AWS_STORAGE_BUCKET_NAME")}.s3.{os.environ.get("AWS_S3_REGION_NAME")}.amazonaws.com',
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
}


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DBNAME"),
        "PORT": os.environ.get("DBPORT"),
        "USER": os.environ.get("DBUSER"),
        "HOST": os.environ.get("DBHOST"),
        "PASSWORD": os.environ.get("DBPASS"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
    "USE_SESSION_AUTH": False,
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": os.environ.get("SECRET_KEY"),
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

MEDIA_URL = f'https://{os.environ.get("AWS_STORAGE_BUCKET_NAME")}.s3.{os.environ.get("AWS_S3_REGION_NAME")}.amazonaws.com/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
# # You can also configure where your static files will be served from S3
STATIC_URL = f'https://{os.environ.get("AWS_STORAGE_BUCKET_NAME")}.s3.{os.environ.get("AWS_S3_REGION_NAME")}.amazonaws.com/static/'

# STATIC_URL = '/static/'


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Health check path
HEALTH_CHECK_PATH = "/health/"
