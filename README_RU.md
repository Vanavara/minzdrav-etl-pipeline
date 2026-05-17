# Minzdrav NSI ETL Pipeline

## Описание проекта
Проект реализует ETL-пайплайн для загрузки и обработки справочника медицинских организаций из НСИ Минздрава РФ.

## Пайплайн:
- автоматически определяет актуальную версию справочника;
- загружает ZIP-архив;
- извлекает JSON;
- сохраняет сырые данные (RAW layer);
- строит Data Vault модель:
    - HUB;
    - Satellite Attributes;
    - Tracking Satellite;
- поддерживает историзацию изменений атрибутов организаций;
- реализует идемпотентную загрузку.

## Архитектура проекта
Проект реализован по принципам:
- ETL pipeline;
- Data Vault 2.0;
- historization / SCD Type 2;
- incremental loading;
- idempotent ingestion.

## Data Vault модель

### RAW Layer
Таблица: nsi.raw_medical_organizations

Содержит:
- полную историю всех загрузок;
- исходные JSON-данные;
- source_version;
- технические поля загрузки.

## HUB
Таблица: nsi.hub_organization

Содержит:
- бизнес-ключ организации (oid);
- стабильный hash key;
- источник данных.

## HUB key
Hash key вычисляется как: sha256(oid)

## Satellite Attributes
Таблица: nsi.sat_organization_attrs

Содержит:
- описательные атрибуты организации;
- hashdiff;
- исторические версии атрибутов.

### Hashdiff 
Hashdiff вычисляется как SHA256 от конкатенации бизнес-атрибутов:
- full_name
- short_name
- ogrn
- inn
- address
- ved_affiliation_id
- inclusion_date
При изменении хотя бы одного атрибута создаётся новая запись в Satellite.

## Tracking Satellite
Таблица: nsi.sat_organization_changes

Содержит:
- историю изменения отдельных атрибутов;
- valid_from;
- valid_to;
- текущее активное значение атрибута.

## Историзация изменений
При изменении значения атрибута:
- предыдущая запись закрывается;
- valid_to заполняется;
- создаётся новая активная запись.

## Особенности реализации historization
Исходная система НСИ не предоставляет:
- business effective date;
- дату фактического изменения атрибутов;
- полноценный API historization.

Из-за этого historization реализована на основе технического времени загрузки (load timestamp approach).


## Почему используется TIMESTAMP вместо DATE
Первоначально valid_from / valid_to были реализованы как DATE.
Однако при загрузке нескольких версий справочника в течение одного календарного дня возникала проблема:
- обе версии получали одинаковую дату;
- временные интервалы historization становились некорректными.

Поэтому тип был изменён на: TIMESTAMP WITH TIME ZONE
Это позволяет корректно обрабатывать:
- несколько загрузок в течение дня;
- последовательные версии справочника;
- временные интервалы SCD Type 2.

## Идемпотентность
Перед загрузкой выполняется проверка: source_version already loaded?
Если версия уже присутствует в RAW layer:
- pipeline завершается;
- повторная загрузка не выполняется.

## Источник данных
Используется публичный web-интерфейс НСИ Минздрава РФ.

## Важное замечание по API
В рамках исследования ресурса был найден endpoint получения metadata справочника.
Однако прямой endpoint скачивания ZIP-архива через Network/API обнаружен не был.
Из-за этого автоматическая загрузка реализована через browser automation с использованием Playwright.

## Используемые технологии
### Backend

- SQLAlchemy 2.0
- Alembic
- PostgreSQL

### Python Version
Для работы проекта требуется Python 3.11 или выше.
Рекомендуемая версия:
- Python 3.12

### ETL / Parsing
- ijson
- Playwright

### Testing
- pytest
- unittest.mock

### Logging
- logging
- TimedRotatingFileHandler

## Установка
### 1. Клонирование проекта
- git clone https://github.com/Vanavara/minzdrav-etl-pipeline

### 2. Создание virtualenv
MacOS / Linux
python3 -m venv .venv

Windows
python -m venv .venv

### 3. Активация virtualenv
MacOS / Linux
source .venv/bin/activate

Windows
.venv\Scripts\activate

### 4. Установка зависимостей
- pip install -r requirements.txt

### 5. Настройка ENV
- Создать .env по шаблону .env.example

### 6. Запустить PostgreSQL
docker compose up -d

### 7. Применение миграций
- alembic upgrade head

### 8. Запуск pipeline
- python -m src.loader

## Логирование
Логи сохраняются в: logs/general.log

Реализовано:
- structured logging;
- daily rotation;
- хранение истории логов.

## Тестирование
Запуск тестов: pytest

### Реализованные тесты:

API
- API available
- timeout handling
- retry handling

Idempotency
- same version skipped
- new version triggers load

Data Vault hashing
- deterministic HUB key
- stable hashdiff
- hashdiff changes on attribute update

Historization
- first version open-ended
- previous version closed
- unchanged attributes ignored
- temporal interval consistency

## Основные особенности реализации
- incremental loading;
- idempotent ETL;
- Data Vault 2.0;
- historization;
- SCD Type 2 behavior;
- browser automation ingestion;
- retry mechanism;
- structured logging;
- automated testing.
