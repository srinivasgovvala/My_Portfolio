#!/usr/bin/env bash
# Build script executed by Vercel during deployment
echo "=== [1/2] Installing Dependencies ==="
python3 -m pip install -r requirements.txt

echo "=== [2/2] Collecting Static Files ==="
python3 manage.py collectstatic --no-input --clear

echo "=== Vercel Build Complete ==="
