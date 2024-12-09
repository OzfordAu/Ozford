import environ
import os

root = environ.Path(__file__) - 2

env = environ.Env()

env_file = str(root.path('.env'))
env.read_env(env_file)

env_mode = env('DJANGO_ENV')

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.dev")

if env_mode == 'production':
    settings_module = 'core.settings.production'
else:
    # print('Wsgi Env', env_mode)
    settings_module = 'core.settings.dev'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

application = get_wsgi_application()
