uwsgi --socket 0.0.0.0:${1} --protocol=http -w app:app
