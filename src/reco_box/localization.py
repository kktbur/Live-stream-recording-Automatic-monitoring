from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Property, QCoreApplication, QLocale, QObject, QTranslator, Signal, Slot
from PySide6.QtQml import QQmlApplicationEngine

from .resources import package_resource
from .storage import Database

LANGUAGES: tuple[tuple[str, str], ...] = (
    ("zh-CN", "简体中文"),
    ("zh-TW", "繁體中文"),
    ("en", "English"),
    ("es", "Español"),
    ("fr", "Français"),
    ("de", "Deutsch"),
    ("pt", "Português"),
    ("ru", "Русский"),
    ("ja", "日本語"),
    ("ko", "한국어"),
)
LANGUAGE_CODES = frozenset(code for code, _ in LANGUAGES)


def tr(source: str) -> str:
    """Translate an application-owned Python message."""
    return QCoreApplication.translate("RecoBox", source)


def supported_system_language(system_name: str) -> str:
    normalized = system_name.replace("_", "-").lower()
    if normalized.startswith(("zh-tw", "zh-hk")):
        return "zh-TW"
    if normalized.startswith("zh"):
        return "zh-CN"
    prefix = normalized.split("-", 1)[0]
    return prefix if prefix in LANGUAGE_CODES else "zh-CN"


def initial_language(database: Database, existing_database: bool, system_name: str) -> str:
    stored = database.get_setting("ui_language", "")
    if stored in LANGUAGE_CODES:
        return stored
    language = "zh-CN" if existing_database else supported_system_language(system_name)
    database.set_setting("ui_language", language)
    return language


class LocalizationController(QObject):
    languageChanged = Signal()

    def __init__(
        self,
        app: QCoreApplication,
        database: Database,
        existing_database: bool,
        translations_dir: Path | None = None,
    ) -> None:
        super().__init__()
        self._app = app
        self._database = database
        self._translations_dir = Path(
            translations_dir or package_resource("translations")
        )
        self._language = initial_language(database, existing_database, QLocale.system().name())
        self._translator: QTranslator | None = None
        self._engine: QQmlApplicationEngine | None = None
        self._install(self._language)

    @Property("QVariantList", constant=True)
    def languages(self) -> list[dict[str, str]]:
        return [{"code": code, "name": name} for code, name in LANGUAGES]

    @Property(str, notify=languageChanged)
    def currentLanguage(self) -> str:
        return self._language

    def set_engine(self, engine: QQmlApplicationEngine) -> None:
        self._engine = engine

    @Slot(str, result=bool)
    def setLanguage(self, code: str) -> bool:
        if code not in LANGUAGE_CODES:
            return False
        if code == self._language:
            return True
        if not self._install(code):
            return False
        self._language = code
        self._database.set_setting("ui_language", code)
        if self._engine is not None:
            self._engine.retranslate()
        self.languageChanged.emit()
        return True

    def _install(self, code: str) -> bool:
        if self._translator is not None:
            self._app.removeTranslator(self._translator)
            self._translator = None
        if code == "zh-CN":
            return True
        translator = QTranslator(self)
        qm_path = self._translations_dir / f"reco_box_{code}.qm"
        if not translator.load(str(qm_path)):
            return False
        self._app.installTranslator(translator)
        self._translator = translator
        return True
