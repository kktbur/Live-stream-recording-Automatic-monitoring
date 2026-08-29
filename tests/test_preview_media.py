import os
import subprocess

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_MEDIA_BACKEND", "ffmpeg")

from PySide6.QtCore import QEventLoop, QTimer, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtMultimedia import QMediaPlayer, QVideoSink

from reco_box.resources import application_resource


def test_qt_ffmpeg_backend_decodes_a_video_frame(tmp_path) -> None:
    ffmpeg = application_resource("runtime", "ffmpeg", "ffmpeg.exe")
    sample = tmp_path / "preview-backend-test.ts"
    subprocess.run(
        [
            str(ffmpeg),
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "lavfi",
            "-i",
            "testsrc=size=160x90:rate=10",
            "-t",
            "1",
            "-c:v",
            "mpeg2video",
            "-f",
            "mpegts",
            str(sample),
        ],
        check=True,
    )

    app = QGuiApplication.instance() or QGuiApplication([])
    player = QMediaPlayer()
    sink = QVideoSink()
    player.setVideoSink(sink)
    loop = QEventLoop()
    valid_frames: list[bool] = []

    def on_frame(frame) -> None:
        valid_frames.append(frame.isValid())
        if frame.isValid():
            loop.quit()

    sink.videoFrameChanged.connect(on_frame)
    timer = QTimer()
    timer.setSingleShot(True)
    timer.timeout.connect(loop.quit)
    timer.start(5_000)
    player.setSource(QUrl.fromLocalFile(str(sample)))
    player.play()
    loop.exec()
    player.stop()
    app.processEvents()

    assert any(valid_frames), f"Qt media backend did not decode a video frame: {player.errorString()}"
