from __future__ import annotations

import shutil

from reco_box import self_check


def test_missing_optional_node_does_not_fail_core_self_check(tmp_path, monkeypatch):
    original_which = shutil.which
    monkeypatch.setattr(
        self_check.shutil,
        "which",
        lambda name: None if name == "node" else original_which(name),
    )
    monkeypatch.setattr(
        self_check.DouyinLiveRecorderResolver,
        "_load_spider",
        lambda self: None,
    )

    assert self_check.run_self_check(tmp_path) == 0

    report = (tmp_path / "self-check.json").read_text(encoding="utf-8")
    assert '"required": false' in report
    assert '"passed": true' in report
