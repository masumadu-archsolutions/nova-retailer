#!/bin/sh
gunicorn app.wsgi:app -b 0.0.0.0:5000
