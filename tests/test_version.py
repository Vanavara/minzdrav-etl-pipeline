# third party
from unittest.mock import patch, MagicMock, mock_open

# project
from src.loader import main


@patch("src.loader.Session")
@patch("src.loader.download_dictionary")
def test_same_version_skipped(
    mock_download_dictionary,
    mock_session,
):
    """
    Existing version should skip pipeline.
    """

    # download mock
    mock_download_dictionary.return_value = (
        "data/raw/test.zip",
        "6.2000",
    )

    # session mock
    mock_session_instance = MagicMock()

    mock_session.return_value.__enter__.return_value = (mock_session_instance)

    # version already exists
    mock_execute_result = MagicMock()

    mock_execute_result.first.return_value = (
        ("existing_hash",)
    )

    mock_session_instance.execute.return_value = (mock_execute_result)

    # execute
    main()

    mock_session_instance.execute.assert_called()

    # pipeline must stop early
    mock_session_instance.bulk_save_objects.assert_not_called()


@patch("src.loader.load_sat_organization_changes")
@patch("src.loader.load_sat_organization_attrs")
@patch("src.loader.load_hub_organizations")
@patch("src.loader.extract_zip")
@patch("src.loader.ijson.items")
@patch("builtins.open", new_callable=mock_open)
@patch("src.loader.Session")
@patch("src.loader.download_dictionary")
def test_new_version_triggers_load(
    mock_download_dictionary,
    mock_session,
    mock_open_file,
    mock_ijson_items,
    mock_extract_zip,
    mock_load_hub,
    mock_load_sat_attrs,
    mock_load_sat_changes,
):
    """
    New version should trigger pipeline loading.
    """

    # download mock
    mock_download_dictionary.return_value = (
        "data/raw/test.zip",
        "6.2001",
    )

    # extract mock
    mock_extract_zip.return_value = (
        "data/extracted/test.json"
    )

    # session mock
    mock_session_instance = MagicMock()

    mock_session.return_value.__enter__.return_value = (mock_session_instance)

    # version does NOT exist
    mock_execute_result = MagicMock()

    mock_execute_result.first.return_value = None

    mock_session_instance.execute.return_value = (mock_execute_result)

    # JSON records mock
    mock_ijson_items.return_value = []

    # execute
    main()

    mock_extract_zip.assert_called_once()

    mock_load_hub.assert_called_once()

    mock_load_sat_attrs.assert_called_once()

    mock_load_sat_changes.assert_called_once()
