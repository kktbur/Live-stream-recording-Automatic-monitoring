from pathlib import Path

from reco_box.media_probe import ProbeResult, media_files, parse_probe_payload, probe_media_files


def test_parse_valid_probe_payload() -> None:
    result = parse_probe_payload(
        {
            "streams": [
                {"codec_type": "video", "codec_name": "h264"},
                {"codec_type": "audio", "codec_name": "aac"},
            ],
            "format": {"duration": "12.5"},
        }
    )

    assert result.valid is True
    assert result.duration_seconds == 12.5
    assert result.codec_summary == "video:h264, audio:aac"


def test_probe_payload_without_streams_is_invalid() -> None:
    result = parse_probe_payload({"streams": [], "format": {}})

    assert result.valid is False
    assert result.error == "文件中没有可识别的音视频流"


def test_segment_files_are_sorted_numerically(tmp_path) -> None:
    for name in ("10.ts", "2.ts", "1.ts"):
        (tmp_path / name).write_bytes(b"x")

    assert [path.name for path in media_files(tmp_path)] == ["1.ts", "2.ts", "10.ts"]


def test_probe_multiple_segments_sums_duration_and_deduplicates_codecs(
    monkeypatch, tmp_path
) -> None:
    paths = [tmp_path / "1.mp4", tmp_path / "2.mp4"]
    for path in paths:
        path.write_bytes(b"x")
    monkeypatch.setattr(
        "reco_box.media_probe.probe_media_file",
        lambda _probe, _path: ProbeResult(True, 5.0, "video:h264, audio:aac"),
    )

    result = probe_media_files(Path("ffprobe.exe"), paths)

    assert result.valid is True
    assert result.duration_seconds == 10.0
    assert result.codec_summary == "video:h264, audio:aac"
