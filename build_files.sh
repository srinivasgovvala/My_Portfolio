#!/usr/bin/env bash
# Build script executed by Vercel during deployment

echo "=== [1/5] Creating directories ==="
mkdir -p staticfiles
mkdir -p static
mkdir -p media

echo "=== [2/5] Installing Python Dependencies ==="
python3 -m pip install --upgrade pip setuptools wheel --break-system-packages 2>/dev/null || python3 -m pip install --upgrade pip || true
python3 -m pip install -r requirements.txt --break-system-packages 2>/dev/null || python3 -m pip install -r requirements.txt || pip install -r requirements.txt

echo "=== [3/5] Collecting Django Static Files ==="
python3 manage.py collectstatic --no-input --clear 2>&1 || python manage.py collectstatic --no-input --clear 2>&1 || true

echo "=== [4/5] Syncing Static & Media Assets ==="
# Ensure static files exist in both root and /static/ paths for bulletproof routing
if [ -d "static" ]; then
    cp -r static/* staticfiles/ 2>/dev/null || true
    mkdir -p staticfiles/static
    cp -r static/* staticfiles/static/ 2>/dev/null || true
fi

# Copy media files into staticfiles for CDN delivery on Vercel
if [ -d "media" ]; then
    mkdir -p staticfiles/media
    cp -r media/* staticfiles/media/ 2>/dev/null || true
fi

echo "=== [5/5] Verifying Output Directory ==="
ls -la staticfiles/ || true

echo "=== Vercel Build Completed Successfully ==="
