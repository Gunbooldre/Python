# fastProject

FastAPI-сервис с Postgres, Alembic и MinIO (S3-совместимое хранилище).

## Стек

| Сервис   | Что это            | Порт        |
|----------|--------------------|-------------|
| api      | FastAPI + uvicorn  | 8000        |
| postgres | База данных        | 5432        |
| minio    | S3-хранилище       | 9000 / 9001 |

## Запуск локально

Нужен только Docker Desktop.

```bash
docker compose up -d --build
```

Прогнать миграции (обязательно при первом старте):

```bash
docker compose exec api alembic upgrade head
```

Создать бакет для файлов (обязательно для роутера `/file`):
открыть http://localhost:9001 (логин/пароль `minioadmin` / `minioadmin`)
и создать бакет с именем из `BUCKET_NAME` (по умолчанию `test`).

Проверить:

- API — http://localhost:8000
- Swagger — http://localhost:8000/docs
- MinIO Console — http://localhost:9001

Остановить:

```bash
docker compose down          # оставить данные
docker compose down -v       # удалить тома postgres и minio
```

## Переменные окружения

Читаются из `.env` (см. `app/config.py`). В `docker-compose.yaml` часть значений
переопределяется под сеть контейнеров — `DATABASE_HOSTNAME=postgres`,
`ENDPOINT_URL=http://minio:9000`.

| Переменная                  | Назначение                                  |
|-----------------------------|---------------------------------------------|
| `DATABASE_*`                | Подключение к Postgres                      |
| `SECRET_KEY`, `ALGORITHM`   | Подпись JWT                                 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Время жизни токена, мин                   |
| `ACCESS_KEY`, `SECRET_KEY_S3` | Ключи MinIO                               |
| `ENDPOINT_URL`              | Адрес S3 изнутри сети контейнеров           |
| `PUBLIC_ENDPOINT_URL`       | Адрес S3 для presigned-ссылок в браузере    |
| `BUCKET_NAME`               | Имя бакета                                  |

## Роутеры

`/posts`, `/users`, `/login`, `/vote`, `/task`, `/file`

## Миграции

```bash
docker compose exec api alembic revision --autogenerate -m "описание"
docker compose exec api alembic upgrade head
docker compose exec api alembic downgrade -1
```

## Тесты

```bash
docker compose exec api pytest
```
