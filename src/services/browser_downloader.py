# third party
from pathlib import Path
from playwright.sync_api import sync_playwright
import re
import time

# project
from src.config.settings import (
    BASE_URL,
    DICTIONARY_OID,
    DOWNLOAD_DIR,
    MAX_RETRIES,
    RETRY_DELAY_SECONDS,
    PAGE_GOTO_TIMEOUT,
    PAGE_WAIT_FOR_TIMEOUT,
    PAGE_EXPECT_DOWNLOAD,
    DROP_DOWN_TIMEOUT
)
from src.logger import logger


def download_dictionary(
    file_format: str = "JSON",
    version: str | None = None,
):
    """
    Downloads dictionary archive from RosMinZdrav NSI.

    Features:
    - automatic version detection;
    - retry mechanism for unstable source;
    - download handling through Playwright.
    """

    DOWNLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    if version:
        url = (
            f"{BASE_URL}/dictionaries/"
            f"{DICTIONARY_OID}/passport/{version}"
        )
    else:
        url = (
            f"{BASE_URL}/dictionaries/"
            f"{DICTIONARY_OID}"
        )

    last_error = None

    for attempt in range(
        1,
        MAX_RETRIES + 1,
    ):

        try:

            with sync_playwright() as p:

                browser = p.chromium.launch(headless=True,)

                context = browser.new_context(
                    accept_downloads=True,
                    ignore_https_errors=True,
                )

                page = context.new_page()

                # open page
                page.goto(
                    url,
                    wait_until="networkidle",
                    timeout=PAGE_GOTO_TIMEOUT,
                )

                page.wait_for_timeout(PAGE_WAIT_FOR_TIMEOUT)

                # detect version
                page_text = (
                    page.locator("body")
                    .inner_text()
                )

                match = re.search(
                    r"\b\d+\.\d+\b",
                    page_text,
                )

                if not match:
                    raise ValueError(
                        "Could not detect dictionary version"
                    )

                actual_version = (
                    match.group(0)
                )

                logger.info(
                    f"Detected version: "
                    f"{actual_version}"
                )

                # download file
                page.get_by_role(
                    "button",
                    name="Скачать",
                ).click()

                dropdown = page.locator(
                    ".ant-dropdown"
                )

                dropdown.wait_for(
                    state="visible",
                    timeout=DROP_DOWN_TIMEOUT,
                    # timeout=10000,
                )

                with page.expect_download(
                    # timeout=30000,
                    timeout=PAGE_EXPECT_DOWNLOAD,

                ) as download_info:

                    dropdown.get_by_text(
                        file_format.upper(),
                        exact=True,
                    ).click()

                download = (
                    download_info.value
                )

                save_path = (
                    DOWNLOAD_DIR
                    / download.suggested_filename
                )

                download.save_as(
                    save_path
                )

                logger.info(
                    f"Downloaded: "
                    f"{save_path}"
                )

                browser.close()

                return (
                    save_path,
                    actual_version,
                )

        except Exception as error:

            last_error = error

            logger.info(
                f"Download attempt "
                f"{attempt}/{MAX_RETRIES} failed: "
                f"{error}"
            )

            if attempt < MAX_RETRIES:

                logger.info(
                    f"Retrying in "
                    f"{RETRY_DELAY_SECONDS} seconds..."
                )

                time.sleep(
                    RETRY_DELAY_SECONDS
                )

    raise RuntimeError(
        f"Dictionary download failed after "
        f"{MAX_RETRIES} attempts"
    ) from last_error
