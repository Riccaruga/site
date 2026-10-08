#!/bin/bash
# Deploy Django to Timeweb virtual hosting (mod_wsgi).
# Run on server via SSH:  bash ~/site/repo/deploy/deploy.sh
# Re-runnable, safe for `media/` (never deleted).
set -e

SITE_DIR="$HOME/site"
REPO_DIR="$SITE_DIR/repo"
PUBLIC_DIR="$SITE_DIR/public_html"
VENV_DIR="$SITE_DIR/venv"
BRANCH="${BRANCH:-master}"

echo "==> [1/6] git pull ($BRANCH)"
cd "$REPO_DIR"
git fetch origin
git checkout "$BRANCH"
git pull origin "$BRANCH"

echo "==> [2/6] venv + pip"
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
pip install -U pip
pip install -r "$REPO_DIR/requirements.txt"

echo "==> [3/6] rsync repo -> public_html (media kept)"
mkdir -p "$PUBLIC_DIR/static" "$PUBLIC_DIR/media"
if command -v rsync >/dev/null 2>&1; then
  rsync -av --delete \
    --exclude='.git/' \
    --exclude='.venv/' --exclude='venv/' \
    --exclude='__pycache__/' \
    --exclude='db.sqlite3' \
    --exclude='.env' \
    --exclude='media/' \
    --exclude='staticfiles/' \
    "$REPO_DIR/" "$PUBLIC_DIR/"
else
  echo "rsync not found, fallback to cp (stale files may remain)"
  cp -rf "$REPO_DIR/." "$PUBLIC_DIR/"
  rm -rf "$PUBLIC_DIR/.git"
fi

echo "==> [4/6] timeweb entrypoint (wsgi.py + .htaccess)"
cp "$PUBLIC_DIR/deploy/wsgi.timeweb.py" "$PUBLIC_DIR/wsgi.py"
cp "$PUBLIC_DIR/deploy/htaccess.timeweb" "$PUBLIC_DIR/.htaccess"

echo "==> [5/6] migrate + collectstatic + check"
python "$PUBLIC_DIR/manage.py" migrate --noinput
python "$PUBLIC_DIR/manage.py" collectstatic --noinput
python "$PUBLIC_DIR/manage.py" check --deploy

echo "==> [6/6] restart mod_wsgi"
touch "$PUBLIC_DIR/wsgi.py"

echo "OK: open http://ct931410.tw1.ru/ and /admin/"
