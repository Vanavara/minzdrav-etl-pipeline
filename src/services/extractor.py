# third party
from pathlib import Path
from zipfile import ZipFile

# project
from src.config.settings import EXTRACT_DIR


def extract_zip(zip_filename: str) -> Path:
    zip_path =  zip_filename

    with ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)

        extracted_files = zip_ref.namelist()

    extracted_json = EXTRACT_DIR / extracted_files[0]

    return extracted_json
