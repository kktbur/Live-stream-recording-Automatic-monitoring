from __future__ import annotations

import os
import tempfile
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from reco_box.app import main


def run() -> None:
    original_exec = QApplication.exec

    def timed_exec(app: QApplication) -> int:
        QTimer.singleShot(1_000, app.quit)
        return original_exec()

    with tempfile.TemporaryDirectory(prefix="reco-box-app-smoke-") as temp_dir:
        os.environ["RECO_BOX_DATA_DIR"] = str(Path(temp_dir) / "data")
        QApplication.exec = timed_exec
        result = main()
        if result != 0:
            raise RuntimeError(f"Reco Box exited with code {result}")
    print("Reco Box application smoke test passed")


if __name__ == "__main__":
    run()
