# Лабораторная работа 1

Репозиторий содержит решение лабораторной № 1 по развёртыванию Apache Airflow через `docker compose` с использованием кастомного Docker-образа и собственного DAG.

## Содержимое

- `Dockerfile` собирает образ на базе `apache/airflow:2.7.1` и копирует DAG в рабочую директорию Airflow.
- `docker-compose.yml` поднимает `postgres`, `airflow-init`, `airflow-webserver` и `airflow-scheduler`.
- `dags/sales_analytics_dag.py` описывает DAG `sales_analytics_pipeline`.

## Что делает DAG

DAG имитирует небольшой ETL/аналитический процесс по продажам:

1. генерирует набор заказов;
2. обогащает записи вычислением выручки;
3. считает дневные метрики;
4. считает метрики по регионам;
5. сохраняет итоговый JSON-отчёт в `reports/sales_report.json` на локальной машине.

## Как запустить локально

Требования:

- установлен Docker;
- установлен Docker Compose V2 (`docker compose`).
- в файле `.env` должен быть указан `AIRFLOW_UID` текущего пользователя.

Команды запуска:

```bash
echo "AIRFLOW_UID=$(id -u)" > .env
docker compose up airflow-init
docker compose up -d
```

После запуска Airflow будет доступен по адресу `http://localhost:8080`.

После успешного запуска DAG отчёт появится в папке `reports/` в корне проекта.

Учётные данные для входа:

- логин: `admin`
- пароль: `admin`

Проверка контейнеров:

```bash
docker ps
```

В списке должны быть контейнеры `postgres`, `airflow-webserver` и `airflow-scheduler` в состоянии `healthy` или `Up`.

Остановка:

```bash
docker compose down
```
