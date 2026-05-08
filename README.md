# Лабораторные работы 2-3

Репозиторий содержит решение лабораторной № 3 по CI/CD. За основу взята лабораторная № 1: Airflow и Postgres остались оркестраторами, а вычисления перенесены в отдельный PySpark job, который запускается через `SparkSubmitOperator`. Для лабораторной № 3 пайплайн реализован в формате GitHub Actions.

## Содержимое

- `Dockerfile` собирает образ Airflow, устанавливает Java, Spark provider и `pyspark`, а также копирует DAG и Spark-скрипты.
- `docker-compose.yml` поднимает `postgres`, `airflow-init`, `airflow-webserver`, `airflow-scheduler`, `spark-master` и `spark-worker`.
- `dags/sales_analytics_dag.py` описывает DAG `sales_analytics_spark_pipeline`, который отправляет Spark job в кластер.
- `spark/sales_analytics_spark_job.py` содержит PySpark-логику расчёта метрик.
- `reports/` хранит итоговый JSON-отчёт.
- `.github/workflows/lab3-ci-cd.yml` описывает CI/CD-пайплайн для GitHub Actions.

## Что делает DAG

DAG `sales_analytics_spark_pipeline` запускает PySpark-приложение, которое:

1. формирует тестовый набор заказов;
2. вычисляет выручку по каждой записи;
3. считает общие метрики по продажам;
4. считает агрегаты по регионам;
5. сохраняет итоговый JSON-отчёт в `reports/sales_report.json`.

## Как запустить локально

Требования:

- установлен Docker;
- установлен Docker Compose V2 (`docker compose`);
- в файле `.env` должен быть указан `AIRFLOW_UID` текущего пользователя.

Команды запуска:

```bash
echo "AIRFLOW_UID=$(id -u)" > .env
docker compose up airflow-init
docker compose up -d
```

После запуска сервисы будут доступны по адресам:

- Airflow UI: `http://localhost:8080`
- Spark Master UI: `http://localhost:8081`
- Spark Worker UI: `http://localhost:8082`
- Spark application UI во время выполнения job: `http://localhost:4040`

Учётные данные для входа:

- логин: `admin`
- пароль: `admin`

Проверка контейнеров:

```bash
docker ps
```

В списке должны быть контейнеры `postgres`, `airflow-webserver`, `airflow-scheduler`, `spark-master` и `spark-worker` в состоянии `healthy` или `Up`.

Дополнительно можно проверить выполнение job в логах scheduler:

```bash
docker compose logs airflow-scheduler
```

Если job стартовала корректно, в логах будет вызов `spark-submit`, а в Spark UI появится зарегистрированное приложение.

Остановка:

```bash
docker compose down
```

## Настройка CI/CD

Для GitHub-версии лабораторной пайплайн вынесен в `.github/workflows/lab3-ci-cd.yml`. В GitHub Actions нет `stages` в GitLab-стиле, поэтому последовательность `test -> build -> deploy` реализована через зависимости `needs`.

Что делает workflow:

- `test` запускается при каждом `push` в любую ветку и проверяет, что директории `dags/` и `spark/`, а также файлы `Dockerfile` и `docker-compose.yml` существуют.
- `build` запускается только после успешного `test`, но автоматически пропускается для веток `feature/*`.
- `deploy` запускается только для веток `main`, `master`, `develop` и `lab3`.
- все jobs выполняются только на self-hosted runner с label `lab3`, что является аналогом тега раннера из задания для GitLab.

### Что нужно настроить в GitHub

1. В репозитории открыть `Settings -> Actions -> Runners`.
2. Зарегистрировать `self-hosted` runner на той машине, где доступен Docker и `docker compose`.
3. Добавить runner пользовательский label `lab3`.
4. Убедиться, что runner запущен и привязан к репозиторию.

### Как проверять выполнение

- workflow будет виден на вкладке `Actions` в GitHub;
- после пуша в `main`, `master`, `develop` или `lab3` должны успешно пройти `test`, `build` и `deploy`;
- после пуша в ветку `feature/*` должен выполниться только `test`;
- состояние контейнеров на self-hosted runner можно проверить командой `docker compose ps`.
