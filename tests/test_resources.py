from pathlib import Path

from reco_box.resources import application_resource, package_resource, upstream_resource


def test_source_resource_locations_exist() -> None:
    assert application_resource("assets", "reco-box.ico").is_file()
    assert package_resource("ui", "Main.qml").is_file()
    assert upstream_resource().joinpath("src", "spider.py").is_file()


def test_frozen_resource_locations(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr("sys.frozen", True, raising=False)
    monkeypatch.setattr("sys._MEIPASS", str(tmp_path), raising=False)

    assert application_resource("runtime") == tmp_path / "runtime"
    assert package_resource("ui", "Main.qml") == tmp_path / "reco_box" / "ui" / "Main.qml"
    assert upstream_resource() == tmp_path / "vendor" / "DouyinLiveRecorder"


def test_packaging_requires_qt_ffmpeg_multimedia_backend() -> None:
    project_root = Path(__file__).parents[1]
    spec = (project_root / "packaging" / "reco_box.spec").read_text(encoding="utf-8")
    build_script = (project_root / "packaging" / "build.ps1").read_text(encoding="utf-8")

    assert "ffmpegmediaplugin.dll" in spec
    assert "ffmpegmediaplugin.dll" in build_script
