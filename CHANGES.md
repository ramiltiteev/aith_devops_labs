# CHANGES

## Лабораторная работа 4

- Добавлены сервисы `loki`, `alloy`, `prometheus` и `grafana` в `docker-compose.yml`.
- Логи Airflow вынесены в `logs/airflow`, логи Spark master/worker — в `logs/spark`.
- Добавлен `alloy.conf` для отправки файловых логов Airflow и Spark в Loki.
- Добавлен `spark/metrics.properties` для Prometheus servlet в Spark.
- Добавлен `prometheus.yml` со сбором метрик Spark master и worker.
- Добавлен provisioning Grafana для datasource’ов Loki/Prometheus и дашборда `Lab 4 Spark Observability`.
