# Minzdrav NSI ETL Pipeline

## Project Description
This project implements an ETL pipeline for loading and processing the Russian Ministry of Health NSI dictionary of medical organizations.

### The pipeline:
- automatically detects the latest dictionary version;
- downloads ZIP archives;
- extracts JSON files;
- stores raw source data (RAW layer);
- builds a Data Vault model:
    - HUB;
    - Satellite Attributes;
    - Tracking Satellite;
- supports historization of organization attribute changes;
- implements idempotent loading.

## Project Architecture

The project is implemented using the following principles:
- ETL pipeline;
- Data Vault 2.0;
- historization / SCD Type 2;
- incremental loading;
- idempotent ingestion.

## Data Vault Model

### RAW Layer
Table: nsi.raw_medical_organizations

Contains:
- full history of all loads;
- original JSON payloads;
- source_version;
- technical load metadata.

### HUB
Table: nsi.hub_organization

Contains:
- business key (oid);
- stable hash key;
- record source.

### HUB Key
Hash key is calculated as: sha256(oid)

### Satellite Attributes
Table: nsi.sat_organization_attrs

Contains:
- descriptive organization attributes;
- hashdiff;
- historical attribute versions.

### Hashdiff

Hashdiff is calculated as SHA256 from concatenated business attributes:
- full_name
- short_name
- ogrn
- inn
- address
- ved_affiliation_id
- inclusion_date

If at least one attribute changes, a new Satellite record is created.

### Tracking Satellite
Table: nsi.sat_organization_changes

Contains:
- attribute-level change history;
- valid_from;
- valid_to;
- current active attribute value.

### Historization Logic
When an attribute value changes:
- previous record is closed;
- valid_to is populated;
- a new active record is created.

### Historization Implementation Notes
The NSI source system does not provide:
- business effective dates;
- real attribute change timestamps;
- historical API support.

Because of this, historization is implemented using technical load timestamps (load timestamp approach).


## Why TIMESTAMP Is Used Instead of DATE

Initially, valid_from / valid_to were implemented as DATE fields.
However, when multiple dictionary versions were loaded within the same calendar day:
- both versions received identical dates;
- historization intervals became invalid.

To solve this issue, the type was changed to: TIMESTAMP WITH TIME ZONE

This allows correct processing of:
- multiple loads during the same day;
- sequential dictionary versions;
- SCD Type 2 temporal intervals.

## Idempotency
Before loading, the pipeline checks: source_version already loaded?
If the version already exists in RAW layer:
- the pipeline stops;
- duplicate loading is skipped.

## Data Source
The project uses the public web interface of the Russian Ministry of Health NSI system.

## Important API Note
During source analysis, a metadata endpoint was identified.
However, a direct ZIP download API endpoint was not exposed through Network/API inspection.
Because of this, automatic downloading is implemented using browser automation with Playwright.

## Technologies

### Backend
- Python 3.12
- SQLAlchemy 2.0
- Alembic
- PostgreSQL

### ETL / Parsing
- ijson
- Playwright

### Testing
- pytest
- unittest.mock

### Logging
- logging
- TimedRotatingFileHandler

## Installation

### 1. Clone repository
git clone https://github.com/Vanavara/minzdrav-etl-pipeline

cd minzdrav

### 2. Create virtual environment
python -m venv .venv

### 3. Activate virtual environment
MacOS / Linux
source .venv/bin/activate

Windows
.venv\Scripts\activate

### 4. Install dependencies
pip install -r requirements.txt

## Environment Configuration
Create .env base on .env.example

## Apply Migrations
alembic upgrade head\

## Run Pipeline
python -m src.loader

## Logging
Logs are stored in: logs/general.log

Implemented features:
- structured logging;
- daily rotation;
- log history retention.

## Testing
Run tests: pytest

### Implemented Tests

API
- API available
- timeout handling
- retry handling

Idempotency
- same version skipped
- new version triggers load

Data Vault Hashing
- deterministic HUB key
- stable hashdiff
- hashdiff changes on attribute update

Historization
- first version open-ended
- previous version closed
- unchanged attributes ignored
- temporal interval consistency

## Main Features
- incremental loading;
- idempotent ETL;
- Data Vault 2.0;
- historization;
- SCD Type 2 behavior;
- browser automation ingestion;
- retry mechanism;
- structured logging;
- automated testing.
