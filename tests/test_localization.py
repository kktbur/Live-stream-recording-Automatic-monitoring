from pathlib import Path

from PySide6.QtGui import QGuiApplication

from reco_box.localization import (
    LANGUAGE_CODES,
    LocalizationController,
    initial_language,
    supported_system_language,
    tr,
)
from reco_box.storage import Database


def test_supported_system_language_mapping() -> None:
    assert supported_system_language("zh_TW") == "zh-TW"
    assert supported_system_language("pt_BR") == "pt"
    assert supported_system_language("de_DE") == "de"
    assert supported_system_language("nl_NL") == "zh-CN"
    assert len(LANGUAGE_CODES) == 10


def test_existing_database_without_language_stays_simplified_chinese(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    assert initial_language(database, True, "de_DE") == "zh-CN"
    assert database.get_setting("ui_language") == "zh-CN"


def test_new_database_follows_supported_system_language_and_persists(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    assert initial_language(database, False, "ja_JP") == "ja"
    assert initial_language(database, True, "de_DE") == "ja"


def test_python_messages_use_the_selected_qt_catalog(tmp_path) -> None:
    app = QGuiApplication.instance() or QGuiApplication([])
    database = Database(tmp_path / "reco_box.db")
    translations = Path(__file__).parents[1] / "src" / "reco_box" / "translations"
    controller = LocalizationController(app, database, True, translations)

    assert controller.setLanguage("en")
    assert tr("找不到直播间") == "Room not found"
    assert controller.setLanguage("zh-CN")
