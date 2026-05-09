# Лабораторная работа 4

Репозиторий содержит решение лабораторной № 4 по наблюдаемости для пайплайна Airflow + Spark. За основу взята предыдущая версия проекта: Airflow запускает PySpark job через `SparkSubmitOperator`, а для лабораторной № 4 добавлены Loki, Alloy, Prometheus и Grafana.

## Содержимое

- `Dockerfile` собирает образ Airflow с Java, Spark provider и `pyspark`.
- `docker-compose.yml` поднимает Postgres, Airflow, Spark master/worker, Loki, Alloy, Prometheus и Grafana.
- `dags/sales_analytics_dag.py` описывает DAG `sales_analytics_spark_pipeline`.
- `spark/sales_analytics_spark_job.py` содержит PySpark-логику расчёта отчёта.
- `spark/metrics.properties` включает Prometheus servlet для Spark master и worker.
- `alloy.conf` описывает сбор файловых логов Airflow и Spark в Loki.
- `prometheus.yml` описывает сбор метрик Spark master и worker.
- `grafana/provisioning/` автоматически создаёт datasource Loki и Prometheus.
- `grafana/dashboards/lab4-observability.json` создаёт дашборд с панелями по Spark-метрикам и логам.

## Что реализовано для ЛР 4

1. Логи Airflow монтируются наружу в `logs/airflow`.
2. Логи Spark master/worker пишутся в `logs/spark/spark-master.log` и `logs/spark/spark-worker.log`.
3. Alloy читает эти файлы и отправляет записи в Loki.
4. Spark master и worker отдают Prometheus-метрики:
   - `http://localhost:8081/metrics/master/prometheus`
   - `http://localhost:8082/metrics/worker/prometheus`
5. Prometheus собирает Spark-метрики каждые 10 секунд.
6. Grafana автоматически получает datasource `Loki` и `Prometheus`.
7. В Grafana создаётся дашборд `Lab 4 Spark Observability` с панелями:
   - состояние Spark targets по запросу `up{job=~"spark-master|spark-worker"}`;
   - сводка Spark master: alive workers, apps, waiting apps;
   - текущая capacity worker: executors, used/free cores;
   - графики CPU cores и memory worker;
   - количество строк логов в минуту из Loki;
   - количество ошибок в логах за последние 5 минут;
   - свежие Spark master/worker logs и Airflow task logs.

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
- Loki: `http://localhost:3100`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`
- Alloy UI: `http://localhost:12345`

Учётные данные Airflow:

- логин: `admin`
- пароль: `admin`

Grafana настроена с anonymous-доступом и ролью `Admin`, поэтому отдельный вход не нужен.

## Проверка

Запустить DAG `sales_analytics_spark_pipeline` в Airflow. После выполнения:

```bash
docker compose ps
docker compose logs alloy
```

В Grafana открыть `Dashboards -> DevOps Labs -> Lab 4 Spark Observability`. 
Скриншоты находятся в папке screenshots

## Остановка

```bash
docker compose down
```
