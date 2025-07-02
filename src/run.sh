#!/bin/bash

echo "▶️  Avvio dei servizi..."

echo "   -> Avvio di Celery worker per TOAD (Python 3.11)..."
PYTHONPATH=/app/TOAD /opt/venv3.11/bin/python -m celery -A TOAD.app.tasks worker --loglevel=info --pool=solo &

echo "   -> Avvio di Uvicorn per TOAD (Python 3.11)..."
PYTHONPATH=/app/TOAD /opt/venv3.11/bin/python -m uvicorn TOAD.app.main:app --host 0.0.0.0 --port 8000 &


echo "   -> Avvio di csDetectorWebService (Python 3.8)..."
/opt/venv3.8/bin/python csDetectorWebService.py &

echo "   -> Avvio di culture-inspector (Python 3.8)..."
/opt/venv3.8/bin/python culture-inspector/runner.py &

echo "   -> Avvio di GUIDO (Python 3.8)..."
/opt/venv3.8/bin/python GUIDO/runner.py &


echo "✅ Tutti i servizi sono stati avviati in background."
echo "   Il container rimarrà attivo. Premi Ctrl+C per terminare."

wait