# Mailing Bot

## Run bot

```
python -m src.handlers
```

## Run cron

```
python -m src.worker.crons -n mailing
```

## To run commands

```
python -m src.worker.commands --help
```

## TODO

* Перевести сессии на нативную хранилку telethon
* Перевести кастомную рассылку на диалог с ботом
