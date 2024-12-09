from .base import *

DEBUG = False
SECRET_KEY = "0uemuf+r%o#3p&$5uk(=l%)wwxs#g*k2q+2s*vf+r85v)aj4^u"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["ozford.edu.np", "www.ucms.edu.np", "beta.ozford.edu.np", "www.ozford.edu.np", "170.64.177.21"]
# WAGTAILADMIN_BASE_URL = "https://ucms.com.np"
WAGTAILADMIN_BASE_URL = "https://ozford.edu.np"

try:
    from .local import *
except ImportError:
    pass
