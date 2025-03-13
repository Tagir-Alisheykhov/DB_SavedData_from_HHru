# Проект: Взаимодействие с API HeadHunter и управление базой данных вакансий

Этот проект предназначен для сбора данных о вакансиях и работодателях с сайта HeadHunter (HH.ru) с использованием их API, обработки этих данных и сохранения их в базе данных PostgreSQL. Проект также предоставляет пользовательский интерфейс для взаимодействия с базой данных.

## Использование
После запуска программы вы увидите меню с доступными командами:

> Добро пожаловать в программу для взаимодействия с базой данных!
Пожалуйста, введите одну или несколько команд представленных ниже:
> - `1` - Получить список всех компаний и количество вакансий у каждой компании.
> - `2` - Получить информацию о всех вакансиях в сжатом виде.
> - `3` - Получить среднюю зарплату по вакансиям.
> - `4` - Получить список всех вакансий, у которых зарплата выше средней.
> - `5` - Получить список всех вакансий по ключевому слову.

## Запуск проекта
```bash
python main.py
```

## Структура проекта
- `data/`: Директория для хранения различных данных.
- `src/`: Основной код проекта.
  - `config.py`: Загрузка чувствительных и конфигурационных данных.
  - `connecting_api.py`: Классы для соединения с API
  - `db_manager.py`: Класс для взаимодействия с БД.
  - `file_processing.py`: Обработка файлов.
  - `processing_vacancies`: Обработка вакансий.
  - `utils.py`: Основной скрипт для пользовательского интерфейса.
- `.env.example`: Шаблон для создания файла с переменными окружения.
- `.gitignore`: Игнорируемые файлы.
- `main.py`: Основной скрипт для запуска программы.

## Основные функции

1. **Сбор данных о работодателях и вакансиях**:
   - Подключение к API HeadHunter для получения информации о работодателях и их вакансиях.
   - Сохранение данных в формате JSON для последующей обработки.

2. **Обработка данных**:
   - Форматирование данных о вакансиях для удобного хранения в базе данных.
   - Подготовка данных для вставки в таблицы базы данных.

3. **Управление базой данных**:
   - Создание таблиц в PostgreSQL для хранения данных о работодателях и вакансиях.
   - Вставка данных в таблицы.
   - Получение данных из базы данных с использованием SQL-запросов.

4. **Пользовательский интерфейс**:
   - Интерактивный интерфейс для выполнения запросов к базе данных.
   - Возможность получения списка компаний, количества вакансий, средней зарплаты и других данных.

## Установка и настройка
### Способ - 1
1. Скопируйте URL-адрес репозитория :
----------------------------------------------------------------
```
https://github.com/Tagir-Alisheykhov/Ai-Detects-Anomalies.git
```
----------------------------------------------------------------
2. Откройте PyCharm или другой используемый вами интерпретатор
и кликните на "Get From VCS".

3. Вставьте скопированный адрес в строку "URL".
4. Далее в строке "Directory" выберите расположение репозитория на вашем ПК. Либо оставьте без изменений.
5. Затем кликните на "Clone" для запуска проекта.
### Способ - 2
1. Откройте "PowerShell" или "Terminal".
2. Введите команду "git clone" и добавьте ссылку на скопированный репозиторий :
--------------------------------------------------------------------------
```
git clone https://github.com/Tagir-Alisheykhov/Ai-Detects-Anomalies.git
```
--------------------------------------------------------------------------
3. Запустите свой интерпретатор.
4. Кликните на "Open".
5. Найдите проект который вы добавили с помощью "git clone URL" (он должен сохраниться в вашей корневой директории).
6. Запустите найденный проект.


## Основные требования

- Python 3.12
- PostgreSQL
- Библиотеки Python: `requests`, `pandas`, `psycopg2`

## Список всех зависимостей
- `black`              25.1.0            The uncompromising code formatter.
- `certifi`            2025.1.31         Python package for providing Mozilla's CA Bundle.
- `charset-normalizer` 3.4.1             The Real First Universal Charset Detector. Open, modern and actively maintained alternative to Chardet.
- `click`              8.1.8             Composable command line interface toolkit
- `colorama`           0.4.6             Cross-platform colored terminal text.
- `flake8`          7.1.2             the modular source code checker: pep8 pyflakes and co
- `idna`               3.10              Internationalized Domain Names in Applications (IDNA)
- `isort`              6.0.1             A Python utility / library to sort Python imports.
- `mccabe`             0.7.0             McCabe checker, plugin for flake8
- `mypy`               1.15.0            Optional static typing for Python
- `mypy-extensions`    1.0.0             Type system extensions for programs checked with the mypy type checker.
- `numpy`              2.2.3             Fundamental package for array computing in Python
- `packaging`          24.2              Core utilities for Python packages
- `pandas`             2.2.3             Powerful data structures for data analysis, time series, and statistics
- `pandas-stubs`       2.2.3.250308      Type annotations for pandas
- `pathspec`           0.12.1            Utility library for gitignore style pattern matching of file paths.
- `platformdirs`       4.3.6             A small Python package for determining appropriate platform-specific dirs, e.g. a user data dir.
- `psycopg2`           2.9.10            psycopg2 - Python-PostgreSQL Database Adapter
- `pycodestyle`        2.12.1            Python style guide checker
- `pyflakes`           3.2.0             passive checker of Python programs
- `python-dateutil`    2.9.0.post0       Extensions to the standard Python datetime module
- `python-dotenv`      1.0.1             Read key-value pairs from a .env file and set them as environment variables
- `pytz`               2025.1            World timezone definitions, modern and historical
- `requests`           2.32.3            Python HTTP for Humans.
- `six`                1.17.0            Python 2 and 3 compatibility utilities
- `types-psycopg2`     2.9.21.20250121   Typing stubs for psycopg2
- `types-pytz`         2025.1.0.20250204 Typing stubs for pytz
- `types-requests`     2.32.0.20250306   Typing stubs for requests
- `typing-extensions`  4.12.2            Backported and Experimental Type Hints for Python 3.8+
- `tzdata`             2025.1            Provider of IANA time zone data
- `urllib3`            2.3.0             HTTP library with thread-safe connection pooling, file post, and more.

## Установка зависимостей
> Активируйте виртуальное окружение с помощью `poetry shell`.

> Используйте `poetry add` для добавления новых зависимостей.

> Используйте `poetry install` для установки всех зависимостей данного проекта.

> Запускайте скрипты через `poetry run`.

## Лицензия
Этот проект не лицензирован.
