from __future__ import annotations

import hashlib
import json
import os
import shutil
import threading
import time
import urllib.request
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable

try:
    from .catalog import CATALOG, ModelArtifact
except ImportError:  # Direct-module unit tests outside ComfyUI.
    from catalog import CATALOG, ModelArtifact


class ModelControlError(RuntimeError):
    pass


@dataclass
class TaskState:
    task_id: str
    action: str
    artifact_id: str
    status: str = "queued"
    bytes_done: int = 0
    bytes_total: int = 0
    message: str = ""
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def public_dict(self) -> dict:
        return asdict(self)


class ModelControl:
    VERSION = "1.0.0"
    RESERVE_BYTES = 10 * 1024**3
    CHUNK_BYTES = 8 * 1024**2

    def __init__(
        self,
        folder_roots: dict[str, Path],
        *,
        opener: Callable = urllib.request.urlopen,
        reserve_bytes: int | None = None,
    ):
        self.folder_roots = {name: Path(path).resolve() for name, path in folder_roots.items()}
        self.opener = opener
        self.reserve_bytes = self.RESERVE_BYTES if reserve_bytes is None else reserve_bytes
        self._lock = threading.RLock()
        self._tasks: dict[str, TaskState] = {}
        self._active_task_id: str | None = None

    @classmethod
    def for_comfy(cls) -> "ModelControl":
        import folder_paths

        categories = {item.folder_category for item in CATALOG.values()}
        roots: dict[str, Path] = {}
        for category in categories:
            paths = folder_paths.get_folder_paths(category)
            if not paths:
                raise ModelControlError(f"ComfyUI has no folder for {category!r}")
            roots[category] = Path(paths[0])
        return cls(roots)

    def capabilities(self) -> dict:
        return {
            "schema": "comfy.model-control-capabilities/1",
            "version": self.VERSION,
            "single_flight": True,
            "resumable": True,
            "verified_size": True,
            "verified_sha256": True,
            "arbitrary_urls": False,
            "arbitrary_paths": False,
            "shell": False,
        }

    def catalog(self) -> dict:
        return {
            "schema": "comfy.model-control-catalog/1",
            "artifacts": [self._artifact_state(item) for item in CATALOG.values()],
        }

    def tasks(self) -> dict:
        with self._lock:
            return {
                "active_task_id": self._active_task_id,
                "tasks": [task.public_dict() for task in self._tasks.values()],
            }

    def task(self, task_id: str) -> dict:
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                raise ModelControlError("unknown task id")
            return task.public_dict()

    def start_download(self, artifact_id: str, expected_sha256: str, confirm: str) -> dict:
        artifact = self._authorized(artifact_id, expected_sha256, confirm, "download")
        if not artifact.downloadable:
            raise ModelControlError("artifact is not downloadable")
        return self._start_task("download", artifact, self._download)

    def start_remove(self, artifact_id: str, expected_sha256: str, confirm: str) -> dict:
        artifact = self._authorized(artifact_id, expected_sha256, confirm, "remove")
        if not artifact.removable:
            raise ModelControlError("artifact is not removable")
        return self._start_task("remove", artifact, self._remove)

    def _authorized(
        self, artifact_id: str, expected_sha256: str, confirm: str, action: str
    ) -> ModelArtifact:
        artifact = CATALOG.get(artifact_id)
        if artifact is None:
            raise ModelControlError("artifact is not allowlisted")
        if expected_sha256 != artifact.sha256:
            raise ModelControlError("digest confirmation does not match catalog")
        if confirm != f"{action}:{artifact_id}":
            raise ModelControlError("confirmation value does not match exact action")
        return artifact

    def _start_task(self, action: str, artifact: ModelArtifact, target: Callable) -> dict:
        with self._lock:
            if self._active_task_id is not None:
                active = self._tasks[self._active_task_id]
                if active.status in {"queued", "running", "verifying"}:
                    raise ModelControlError(f"mutation task {active.task_id} is already active")
            task = TaskState(
                task_id=str(uuid.uuid4()),
                action=action,
                artifact_id=artifact.artifact_id,
                bytes_total=artifact.size_bytes,
            )
            self._tasks[task.task_id] = task
            self._active_task_id = task.task_id
            thread = threading.Thread(
                target=self._run_task,
                args=(task, artifact, target),
                name=f"model-control-{action}-{artifact.artifact_id}",
                daemon=True,
            )
            thread.start()
            return task.public_dict()

    def _run_task(self, task: TaskState, artifact: ModelArtifact, target: Callable) -> None:
        self._update(task, status="running")
        try:
            target(task, artifact)
            self._update(task, status="success", message="verified")
        except Exception as exc:
            self._update(task, status="error", message=str(exc))
        finally:
            with self._lock:
                if self._active_task_id == task.task_id:
                    self._active_task_id = None

    def _download(self, task: TaskState, artifact: ModelArtifact) -> None:
        target = self._target(artifact)
        target.parent.mkdir(parents=True, exist_ok=True)
        partial = target.with_name(target.name + ".part")
        receipt = target.with_name(target.name + ".model-control.json")
        if target.exists():
            raise ModelControlError("final target already exists")
        offset = partial.stat().st_size if partial.exists() else 0
        if offset > artifact.size_bytes:
            raise ModelControlError("partial file exceeds expected size")
        remaining = artifact.size_bytes - offset
        free = shutil.disk_usage(target.parent).free
        if free - remaining < self.reserve_bytes:
            raise ModelControlError(
                f"insufficient free space: need {remaining + self.reserve_bytes} bytes"
            )

        request = urllib.request.Request(artifact.url)
        if offset:
            request.add_header("Range", f"bytes={offset}-")
        response = self.opener(request, timeout=60)
        status = getattr(response, "status", response.getcode())
        if offset and status != 206:
            response.close()
            offset = 0
            request = urllib.request.Request(artifact.url)
            response = self.opener(request, timeout=60)

        mode = "ab" if offset else "wb"
        self._update(task, bytes_done=offset)
        try:
            with response, partial.open(mode) as handle:
                while True:
                    chunk = response.read(self.CHUNK_BYTES)
                    if not chunk:
                        break
                    handle.write(chunk)
                    offset += len(chunk)
                    self._update(task, bytes_done=offset)
                handle.flush()
                os.fsync(handle.fileno())
        except Exception:
            # The verified prefix remains available for an exact resume.
            raise

        if partial.stat().st_size != artifact.size_bytes:
            raise ModelControlError(
                f"size mismatch: got {partial.stat().st_size}, expected {artifact.size_bytes}"
            )
        self._update(task, status="verifying", bytes_done=artifact.size_bytes)
        digest = self._sha256(partial)
        if digest != artifact.sha256:
            raise ModelControlError(f"sha256 mismatch: got {digest}")
        os.replace(partial, target)
        self._write_receipt(receipt, artifact)

    def _remove(self, task: TaskState, artifact: ModelArtifact) -> None:
        target = self._target(artifact)
        if not target.exists():
            raise ModelControlError("target does not exist")
        if target.is_symlink() or not target.is_file():
            raise ModelControlError("target is not a regular file")
        if target.stat().st_size != artifact.size_bytes:
            raise ModelControlError("target size does not match allowlist")
        self._update(task, status="verifying", bytes_done=artifact.size_bytes)
        digest = self._sha256(target)
        if digest != artifact.sha256:
            raise ModelControlError(f"sha256 mismatch: got {digest}")
        target.unlink()
        receipt = target.with_name(target.name + ".model-control.json")
        if receipt.exists() and not receipt.is_symlink():
            receipt.unlink()

    def _artifact_state(self, artifact: ModelArtifact) -> dict:
        target = self._target(artifact)
        partial = target.with_name(target.name + ".part")
        state = artifact.public_dict()
        state.update(
            {
                "installed": target.exists(),
                "installed_size_bytes": target.stat().st_size if target.exists() else None,
                "partial_size_bytes": partial.stat().st_size if partial.exists() else 0,
                "size_matches": target.exists() and target.stat().st_size == artifact.size_bytes,
            }
        )
        return state

    def _target(self, artifact: ModelArtifact) -> Path:
        root = self.folder_roots.get(artifact.folder_category)
        if root is None:
            raise ModelControlError(f"folder category {artifact.folder_category!r} is unavailable")
        target = (root / artifact.filename).resolve()
        if target.parent != root:
            raise ModelControlError("target escapes its ComfyUI model folder")
        if target.is_symlink():
            raise ModelControlError("symlink targets are refused")
        return target

    def _update(self, task: TaskState, **changes) -> None:
        with self._lock:
            for name, value in changes.items():
                setattr(task, name, value)
            task.updated_at = time.time()

    @staticmethod
    def _sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            while chunk := handle.read(8 * 1024**2):
                digest.update(chunk)
        return digest.hexdigest()

    @staticmethod
    def _write_receipt(path: Path, artifact: ModelArtifact) -> None:
        payload = {
            "schema": "comfy.model-control-receipt/1",
            "artifact_id": artifact.artifact_id,
            "filename": artifact.filename,
            "size_bytes": artifact.size_bytes,
            "sha256": artifact.sha256,
            "source_revision": artifact.source_revision,
            "verified_at": time.time(),
        }
        temporary = path.with_name(path.name + ".tmp")
        temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(temporary, path)
