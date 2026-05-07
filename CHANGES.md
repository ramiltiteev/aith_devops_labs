# CHANGES

## Лабораторная работа 2

- `Dockerfile` обновлён: добавлены `procps`, `default-jre`, `apache-airflow-providers-apache-spark` и `pyspark`, а также копирование директории `spark/`.
- `docker-compose.yml` расширен сервисами `spark-master` и `spark-worker`, пробросом Spark UI и volume для `spark/`.
- DAG из лабораторной № 1 заменён на оркестрацию Spark job через `SparkSubmitOperator`.
- Добавлен PySpark-скрипт `spark/sales_analytics_spark_job.py` для расчёта отчёта по продажам.
- `README.md` обновлён под новый процесс запуска и проверки Airflow + Spark.
