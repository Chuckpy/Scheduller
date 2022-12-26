from __future__ import absolute_import, unicode_literals
from celery import Celery
from os import getenv


def generate_celery_app():
    app = Celery("proj", broker=getenv("CELERY_BROKER_URL"), include=["proj.tasks"])

    app.conf.result_backend = getenv("CELERY_BROKER_URL")

    app.config_from_object = "proj.celeryconfig"  # ¯\_(ツ)_/¯

    app.conf.beat_schedule = {}

    app.conf.beat_schedule = {
        "add-30-s": {"task": "proj.tasks.add", "schedule": 30.0, "args": (16, 16)},
    }

    return app


celery_app = generate_celery_app()
