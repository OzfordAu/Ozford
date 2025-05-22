from .base import *

DEBUG = False
SECRET_KEY = "0uemuf+r%o#3p&$5uk(=l%)wwxs#g*k2q+2s*vf+r85v)aj4^u"
HTML_MINIFY = True

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["ozford.edu.au", "beta.ozford.edu.au", "www.ozford.edu.au"]
# WAGTAILADMIN_BASE_URL = "https://ucms.com.np"
WAGTAILADMIN_BASE_URL = "https://ozford.edu.au"

try:
    from .local import *
except ImportError:
    pass
