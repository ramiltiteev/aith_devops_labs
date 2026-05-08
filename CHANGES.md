# CHANGES

## Лабораторная работа 3

- Добавлен workflow GitHub Actions `.github/workflows/lab3-ci-cd.yml` как адаптация задания по CI/CD под GitHub-репозиторий.
- В workflow реализованы этапы `test`, `build` и `deploy` с зависимостями `needs`.
- `test` настроен на запуск во всех ветках и проверяет наличие директорий `dags/`, `spark/` и базовых файлов проекта.
- `build` автоматически пропускается для веток `feature/*`.
- `deploy` выполняется только для веток `main`, `master`, `develop` и `lab3`.
- Все jobs привязаны к self-hosted runner с label `lab3`, что заменяет тегированный runner из GitLab-версии задания.
- `README.md` дополнен инструкцией по настройке self-hosted runner и описанием логики GitHub Actions pipeline.
