from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-8(#(z54*=5c2e72uu92h^0kgpyk91mvuk*qmfnryufs7oj9umc"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# WAGTAILADMIN_BASE_URL = "http://localhost:8000"
WAGTAILADMIN_BASE_URL = "http://localhost:8000"

try:
    from .local import *
except ImportError:
    pass
