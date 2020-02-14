#!/usr/bin/env python
import os
import sys
import environ

if __name__ == "__main__":
    environ.Env.read_env()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intradarmajaya.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
