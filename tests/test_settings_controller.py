import pytest

from reco_box.app import _connect_resolver_rate_limit_settings
from reco_box.monitor import MonitoringCoordinator
from reco_box.room_model import RoomListModel
from reco_box.storage import Database
from reco_box.view_models import SettingsController


def _save(settings: SettingsController, root: str, maximum: str, platform: str, interval: str) -> str:
    return settings.saveDefaults(
        root,
        "ts",
        "原画",
        "300",
        False,
        "5",
        "1",
        "",
        maximum,
        platform,
        interval,
    )


def test_settings_persist_resolver_limits_and_update_monitor(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    settings = SettingsController(database)
    rooms = RoomListModel(database)
    coordinator = MonitoringCoordinator(rooms, object())
    _connect_resolver_rate_limit_settings(settings, coordinator)

    assert _save(settings, str(tmp_path / "records"), "8", "3", "0") == ""

    assert settings.resolverMaxConcurrency == 8
    assert settings.resolverPlatformConcurrency == 3
    assert settings.resolverPlatformIntervalSeconds == 0
    assert coordinator.rate_limiter.config.max_resolver_concurrency == 8
    assert coordinator.rate_limiter.config.default_platform_concurrency == 3
    assert coordinator.rate_limiter.config.default_platform_interval_seconds == 0
    assert coordinator.resolver_pool.maxThreadCount() == 8
    assert database.get_setting("resolver_max_concurrency") == "8"
    assert database.get_setting("resolver_platform_concurrency") == "3"
    assert database.get_setting("resolver_platform_interval_seconds") == "0"


@pytest.mark.parametrize(
    ("maximum", "platform", "interval", "message"),
    [
        ("0", "1", "1", "Resolver 最大并发"),
        ("4", "0", "1", "单平台并发"),
        ("4", "1", "3601", "平台冷却"),
        ("4", "1", "not-a-number", "解析限制参数必须是整数"),
    ],
)
def test_settings_reject_invalid_resolver_limits(
    tmp_path, maximum: str, platform: str, interval: str, message: str
) -> None:
    database = Database(tmp_path / "reco_box.db")
    settings = SettingsController(database)

    error = _save(settings, str(tmp_path / "records"), maximum, platform, interval)

    assert message in error
    assert database.get_setting("resolver_max_concurrency") == ""
    assert database.get_setting("resolver_platform_concurrency") == ""
    assert database.get_setting("resolver_platform_interval_seconds") == ""
