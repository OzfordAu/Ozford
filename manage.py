#!/usr/bin/env python
import environ
import os
import sys

root = environ.Path(__file__) - 1

# Load environment variables from the .env file in the root directory
env = environ.Env()
env_file = str(root.path('.env'))
env.read_env(env_file)

# Retrieve the value of the DJANGO_ENV environment variable
env_mode = env('DJANGO_ENV')

if __name__ == "__main__":
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.dev")
    if env_mode == 'production':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.production")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
