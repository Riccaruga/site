"""
WSGI entrypoint for Timeweb virtual hosting (mod_wsgi).

Install location on server (NOT in git checkout):
    ~/site/public_html/wsgi.py  <- copy of this file

Deploy copies it:
    cp ~/site/public_html/deploy/wsgi.timeweb.py ~/site/public_html/wsgi.py

What it does:
  1. Loads secrets from ~/site/.env (chmod 600, NOT in git).
  2. Activates ~/site/venv.
  3. Adds ~/site/public_html to sys.path so `config.settings` imports.
  4. Exposes `application` for mod_wsgi.
"""
import os
import sys

SITE_DIR = os.path.expanduser('~/site')
PUBLIC_HTML = os.path.join(SITE_DIR, 'public_html')
VENV_DIR = os.path.join(SITE_DIR, 'venv')
ENV_FILE = os.path.join(SITE_DIR, '.env')


def _load_dotenv(path):
    """Minimal .env loader without extra deps: KEY=VALUE, ignores # and quotes."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, _, val = line.partition('=')
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = val
    except FileNotFoundError:
        pass


_load_dotenv(ENV_FILE)

# 1. Activate virtualenv (activate_this.py exists in venv created by `python -m venv`)
activate_this = os.path.join(VENV_DIR, 'bin', 'activate_this.py')
if os.path.exists(activate_this):
    exec(open(activate_this).read(), {'__file__': activate_this})
else:
    # Fallback: put venv site-packages on sys.path (Timeweb layout)
    import glob as _glob
    for _p in _glob.glob(os.path.join(VENV_DIR, 'lib', 'python*', 'site-packages')):
        if _p not in sys.path:
            sys.path.insert(0, _p)

# 2. Project root (manage.py lives here after rsync from repo)
if PUBLIC_HTML not in sys.path:
    sys.path.insert(1, PUBLIC_HTML)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
