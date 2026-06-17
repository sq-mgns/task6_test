# Railway bot

Это отдельная версия бота для деплоя не в Yandex Cloud, а в Docker-контейнере на Railway.

Здесь используется `long polling`, поэтому:

1. не нужен `API Gateway`;
2. не нужен webhook;
3. не нужен `Yandex Cloud` для приема сообщений.

## Что делает бот

1. на `/start` и `/help` отправляет текст по шаблону;
2. на голосовое сообщение отвечает текстом:

```text
тест тест раз два три проверка
```

3. на картинку отвечает текстом:

```text
доброе утро

где
```

## Файлы

1. `bot.py` — код бота;
2. `requirements.txt` — зависимости;
3. `Dockerfile` — сборка контейнера.

## Локальный запуск

В PowerShell:

```powershell
$env:TELEGRAM_TOKEN="<токен_бота>"
python bot.py
```

В WSL или Linux:

```bash
export TELEGRAM_TOKEN="<токен_бота>"
python3 bot.py
```

## Сборка Docker-образа локально

Из папки `task6/railway-bot`:

```bash
docker build -t task6-railway-bot .
docker run --rm -e TELEGRAM_TOKEN="<токен_бота>" task6-railway-bot
```

## Как задеплоить на Railway

### Вариант через GitHub

1. Загрузи проект в GitHub.
2. В Railway создай новый проект через `Deploy from GitHub repo`.
3. Подключи репозиторий.
4. Для сервиса укажи `Root Directory`:

```text
task6/railway-bot
```

5. В переменных сервиса добавь:

```text
TELEGRAM_TOKEN=<токен_бота>
```

6. Railway сам увидит `Dockerfile` и соберет контейнер.
7. Публичный домен не нужен, потому что бот работает через polling.

### Вариант через Railway CLI

Из папки `task6/railway-bot`:

```bash
railway login
railway init
railway up
```

После этого в Railway тоже нужно добавить переменную:

```text
TELEGRAM_TOKEN=<токен_бота>
```

## Что важно

Если раньше у этого бота был webhook, его лучше удалить, чтобы Telegram не продолжал слать события на старый адрес.

Пример для PowerShell:

```powershell
$botToken = "<токен_бота>"
Invoke-RestMethod -Method Post -Uri "https://api.telegram.org/bot$botToken/deleteWebhook"
```

После удаления webhook бот на Railway будет получать сообщения сам через polling.
