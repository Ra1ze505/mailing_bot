# Mailing Bot

## Run bot

```
python -m src.handlers
```

## Run celery

```
celery -A src.worker.tasks.app worker -B -E
```

```
1) реализовать рассылку
2) курс валют +
3) last handler
4) закрывается клиент +
```
