"""
Legacy Vercel serverless WSGI entrypoint.

Production is moving to Fly.io gunicorn via config.wsgi (see docs/migrate-off-vercel.md).
Keep this module only for temporary dual-run / rollback on Vercel.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = get_wsgi_application()
