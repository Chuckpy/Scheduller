pip install -r app/requirements/flower_requirements.txt;
echo "Running Beat schedulle . . ."
cd app/src/
python3.10 -m celery -A proj flower --port=${FLOWER_PORT}