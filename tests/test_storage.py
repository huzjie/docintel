# -*- coding: utf-8 -*-
import tempfile
from pathlib import Path

from docintel.storage.store import DocStore
from docintel.types import Document


def test_store():
    with tempfile.TemporaryDirectory() as d:
        s = DocStore(Path(d) / "db.db")
        doc = Document(source="x", format="text", title="t", text="body")
        s.save_document(doc)
        s.record_task("x", "success")
        tasks = s.recent_tasks(10)
        assert len(tasks) == 1
        assert tasks[0]["status"] == "success"
