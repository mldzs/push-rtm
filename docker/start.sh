#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset

cd docs && make html && cd ..
python /app/manage.py collectstatic --noinput
if [ "${COMPRESS_ENABLED}" = true ]; then
    python /app/manage.py compress --extension=.html
fi
/usr/local/bin/gunicorn ureport.wsgi --bind 0.0.0.0:8000 --log-level=debug --access-logfile=./gunicorn.access --error-logfile=./gunicorn.errors --capture-output --chdir=/app
