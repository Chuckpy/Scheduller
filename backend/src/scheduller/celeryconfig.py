# List of modules to import when the Celery worker starts.
imports = ("proj.tasks",)

result_backend = "mongodb://localhost:27017/"
mongodb_backend_settings = {
    "database": "jobs",
    "taskmeta_collection": "my_taskmeta_collection",
}

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "America/Sao_Paulo"
enable_utc = True
result_expires = 3600
