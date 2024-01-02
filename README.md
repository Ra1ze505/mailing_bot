# Mailing Bot

## Run bot

```
python -m src.handlers
```

## Run celery

```
celery -A src.worker.tasks.app worker -B -E
```
