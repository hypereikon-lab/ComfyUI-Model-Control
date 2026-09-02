from __future__ import annotations

import hashlib
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from catalog import ModelArtifact
from model_control import ModelControl, ModelControlError


class FakeResponse:
    def __init__(self, payload: bytes, status: int = 200):
        self.payload = payload
        self.status = status
        self.offset = 0

    def read(self, size: int) -> bytes:
        chunk = self.payload[self.offset : self.offset + size]
        self.offset += len(chunk)
        return chunk

    def getcode(self):
        return self.status

    def close(self):
        return None

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None


class ModelControlTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.payload = b"verified model bytes"
        self.artifact = ModelArtifact(
            "test.model",
            "test",
            "test",
            "diffusion_models",
            "model.safetensors",
            "https://example.invalid/model.safetensors",
            len(self.payload),
            hashlib.sha256(self.payload).hexdigest(),
            "0" * 40,
        )

    def tearDown(self):
        self.temp.cleanup()

    def control(self, payload: bytes | None = None) -> ModelControl:
        value = self.payload if payload is None else payload
        return ModelControl(
            {"diffusion_models": self.root},
            opener=lambda *_args, **_kwargs: FakeResponse(value),
            reserve_bytes=0,
        )

    def wait(self, control: ModelControl, task_id: str) -> dict:
        for _ in range(100):
            task = control.task(task_id)
            if task["status"] not in {"queued", "running", "verifying"}:
                return task
            time.sleep(0.01)
        self.fail("task did not finish")

    def test_unknown_artifact_is_refused(self):
        control = self.control()
        with self.assertRaisesRegex(ModelControlError, "allowlisted"):
            control.start_download("unknown", "0" * 64, "download:unknown")

    def test_download_is_verified_and_atomic(self):
        control = self.control()
        with patch.dict("model_control.CATALOG", {self.artifact.artifact_id: self.artifact}, clear=True):
            task = control.start_download(
                self.artifact.artifact_id,
                self.artifact.sha256,
                f"download:{self.artifact.artifact_id}",
            )
            result = self.wait(control, task["task_id"])
        self.assertEqual(result["status"], "success")
        self.assertEqual((self.root / self.artifact.filename).read_bytes(), self.payload)
        self.assertFalse((self.root / (self.artifact.filename + ".part")).exists())

    def test_bad_digest_never_finalizes(self):
        control = self.control(b"wrong")
        with patch.dict("model_control.CATALOG", {self.artifact.artifact_id: self.artifact}, clear=True):
            task = control.start_download(
                self.artifact.artifact_id,
                self.artifact.sha256,
                f"download:{self.artifact.artifact_id}",
            )
            result = self.wait(control, task["task_id"])
        self.assertEqual(result["status"], "error")
        self.assertFalse((self.root / self.artifact.filename).exists())

    def test_remove_requires_verified_exact_file(self):
        target = self.root / self.artifact.filename
        target.write_bytes(self.payload)
        control = self.control()
        with patch.dict("model_control.CATALOG", {self.artifact.artifact_id: self.artifact}, clear=True):
            task = control.start_remove(
                self.artifact.artifact_id,
                self.artifact.sha256,
                f"remove:{self.artifact.artifact_id}",
            )
            result = self.wait(control, task["task_id"])
        self.assertEqual(result["status"], "success")
        self.assertFalse(target.exists())

    def test_wrong_confirmation_is_refused(self):
        control = self.control()
        with patch.dict("model_control.CATALOG", {self.artifact.artifact_id: self.artifact}, clear=True):
            with self.assertRaisesRegex(ModelControlError, "confirmation"):
                control.start_download(self.artifact.artifact_id, self.artifact.sha256, "yes")

    def test_catalog_and_remove_cover_every_configured_root(self):
        secondary = self.root / "secondary"
        secondary.mkdir()
        target = secondary / self.artifact.filename
        target.write_bytes(self.payload)
        control = ModelControl(
            {"diffusion_models": (self.root, secondary)},
            opener=lambda *_args, **_kwargs: FakeResponse(self.payload),
            reserve_bytes=0,
        )
        with patch.dict("model_control.CATALOG", {self.artifact.artifact_id: self.artifact}, clear=True):
            state = control.catalog()["artifacts"][0]
            task = control.start_remove(
                self.artifact.artifact_id,
                self.artifact.sha256,
                f"remove:{self.artifact.artifact_id}",
            )
            result = self.wait(control, task["task_id"])
        self.assertTrue(state["installed"])
        self.assertEqual(state["installed_copies"], 1)
        self.assertEqual(result["status"], "success")
        self.assertFalse(target.exists())

    def test_remove_validates_all_copies_before_deleting_any(self):
        secondary = self.root / "secondary"
        secondary.mkdir()
        primary_target = self.root / self.artifact.filename
        secondary_target = secondary / self.artifact.filename
        primary_target.write_bytes(self.payload)
        secondary_target.write_bytes(b"same-size-wrong-bytes")
        control = ModelControl(
            {"diffusion_models": (self.root, secondary)}, reserve_bytes=0
        )
        with patch.dict("model_control.CATALOG", {self.artifact.artifact_id: self.artifact}, clear=True):
            task = control.start_remove(
                self.artifact.artifact_id,
                self.artifact.sha256,
                f"remove:{self.artifact.artifact_id}",
            )
            result = self.wait(control, task["task_id"])
        self.assertEqual(result["status"], "error")
        self.assertTrue(primary_target.exists())
        self.assertTrue(secondary_target.exists())


if __name__ == "__main__":
    unittest.main()
