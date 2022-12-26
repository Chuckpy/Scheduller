pip install -r app/requirements/celery_requirements.txt;
echo "Celery Running . . ."
cd app/src/
python3 -m celery -A proj worker --beat --loglevel=info 
