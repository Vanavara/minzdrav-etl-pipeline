# third party
from pathlib import Path
import pytest
from unittest.mock import MagicMock, patch
from playwright.sync_api import TimeoutError

# project
from src.services.browser_downloader import download_dictionary


@patch("src.services.browser_downloader.sync_playwright")
def test_api_available(mock_playwright):
    """
    Positive download scenario.

    Checks:
    - page successfully opened;
    - version successfully detected;
    - file successfully downloaded;
    - function returned expected values.
    """

    # download mock
    mock_download = MagicMock()

    mock_download.suggested_filename = (
        "dictionary.zip"
    )

    # download context manager
    mock_download_context = MagicMock()
    mock_download_context.value = (mock_download)
    mock_expect_download = MagicMock()
    mock_expect_download.__enter__.return_value = (mock_download_context)
    mock_expect_download.__exit__.return_value = (None)

    # page mock
    mock_page = MagicMock()

    # successful page content
    mock_body_locator = MagicMock()

    mock_body_locator.inner_text.return_value = ("Версия 6.2000")

    def locator_side_effect(selector):
        if selector == "body":
            return mock_body_locator

        mock_dropdown = MagicMock()
        return mock_dropdown

    mock_page.locator.side_effect = (locator_side_effect)

    mock_page.expect_download.return_value = (mock_expect_download)

    # browser/context mocks
    mock_context = MagicMock()
    mock_context.new_page.return_value = (mock_page)
    mock_browser = MagicMock()
    mock_browser.new_context.return_value = (mock_context)

    # playwright mock
    mock_playwright_instance = MagicMock()

    mock_playwright_instance.chromium.launch.return_value = (mock_browser)
    mock_playwright.return_value.__enter__.return_value = (mock_playwright_instance)

    # execute
    zip_path, version = download_dictionary()

    assert version == "6.2000"

    assert zip_path == Path("data/raw/dictionary.zip")

    mock_page.goto.assert_called_once()

    mock_download.save_as.assert_called_once()



@patch("src.services.browser_downloader.sync_playwright")
def test_api_timeout(mock_playwright):
    """
    Timeout scenario.

    Checks:
    - timeout triggers retry mechanism;
    - all retry attempts are executed;
    - RuntimeError is raised after retries exhausted.
    """

    # page mock
    mock_page = MagicMock()

    mock_page.goto.side_effect = (TimeoutError("Connection timeout"))

    # context/browser mocks
    mock_context = MagicMock()
    mock_context.new_page.return_value = (mock_page)
    mock_browser = MagicMock()
    mock_browser.new_context.return_value = (mock_context)

    # playwright mock
    mock_playwright_instance = (MagicMock())

    mock_playwright_instance.chromium.launch.return_value = (mock_browser)

    mock_playwright.return_value.__enter__.return_value = (mock_playwright_instance)

    with pytest.raises(RuntimeError):
        download_dictionary()

    # retry count check
    assert mock_page.goto.call_count == 3


@patch("src.services.browser_downloader.sync_playwright")
def test_api_500_error(mock_playwright):
    """
    Server error scenario.

    Checks:
    - server-side error correctly raises exception;
    - pipeline stops.
    """

    # page mock
    mock_page = MagicMock()

    mock_page.goto.side_effect = (Exception("500 Internal Server Error"))

    # context/browser mocks
    mock_context = MagicMock()
    mock_context.new_page.return_value = (mock_page)
    mock_browser = MagicMock()
    mock_browser.new_context.return_value = (mock_context)

    # playwright mock
    mock_playwright_instance = MagicMock()

    mock_playwright_instance.chromium.launch.return_value = (mock_browser)

    mock_playwright.return_value.__enter__.return_value = (mock_playwright_instance)

    with pytest.raises(Exception):
        download_dictionary()
