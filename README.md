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
3. `Dockerfile` — сборка контейнера;
4. `voice.ogg` — необязательная голосовая заготовка для ответа на обычный текст.

## Как теперь отвечает на обычный текст

Если пользователь отправляет обычное текстовое сообщение, бот пытается отправить в ответ голосовое сообщение.

Поддерживаются два варианта:

1. через переменную окружения `VOICE_FILE_ID`;
2. через локальный файл `voice.ogg` внутри папки проекта.

Если ни `VOICE_FILE_ID`, ни `voice.ogg` нет, бот отправит текст:

```text
Голосовая заготовка не найдена
```

## Как проще всего сделать голосовую заготовку

Самый простой вариант — подготовить файл `voice.ogg`.

Что сделать:

1. запиши короткое голосовое сообщение с нужной фразой;
2. сохрани его как файл `voice.ogg`;
3. положи файл рядом с `bot.py`, то есть сюда:

```text
task6/railway-bot/voice.ogg
```

После этого Docker автоматически заберет его в контейнер.

## Альтернатива через VOICE_FILE_ID

Если у тебя уже есть `file_id` голосового сообщения Telegram, можно вообще не класть файл в проект.

Тогда в переменные Railway добавь:

```text
VOICE_FILE_ID=<file_id_голосового_сообщения>
```

В этом случае бот будет отправлять голосовое прямо по `file_id`.

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

Если хочешь проверить вариант через `VOICE_FILE_ID` локально:

```powershell
$env:TELEGRAM_TOKEN="<токен_бота>"
$env:VOICE_FILE_ID="<file_id>"
python bot.py
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

Если хочешь отправлять голосовое без файла в репозитории, дополнительно добавь:

```text
VOICE_FILE_ID=<file_id_голосового_сообщения>
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

При необходимости также:

```text
VOICE_FILE_ID=<file_id_голосового_сообщения>
```

## Что важно

Если раньше у этого бота был webhook, его лучше удалить, чтобы Telegram не продолжал слать события на старый адрес.

Пример для PowerShell:

```powershell
$botToken = "<токен_бота>"
Invoke-RestMethod -Method Post -Uri "https://api.telegram.org/bot$botToken/deleteWebhook"
```

После удаления webhook бот на Railway будет получать сообщения сам через polling.
