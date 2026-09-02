# ComfyUI Model Control

A UI-less, allowlist-only download and retirement plane for large model files
on a remote ComfyUI host.

The laboratory ComfyUI origin is reachable through Cloudflare Access, but the
host terminal is not. ComfyUI-Manager intentionally refuses models absent from
its central catalog. This extension fills only that gap without exposing a
shell, arbitrary URL downloader, filesystem browser, or generic delete route.

## Safety model

Every accepted artifact is compiled into `catalog.py` with:

- immutable public source revision;
- exact URL;
- exact byte count and SHA-256 digest;
- ComfyUI folder category and filename;
- explicit permission to download and/or retire.

Downloads are single-flight, resumable, written to `*.part`, verified, and
atomically finalized. Removal hashes the existing file and refuses any digest
mismatch. Every ComfyUI root registered for the artifact's folder category is
reconciled: downloads refuse pre-existing copies anywhere, while retirement
validates every copy before deleting any of them. Ten GiB of reserve space is
kept by default.

## HTTP contract

```text
GET  /model-control/v1/capabilities
GET  /model-control/v1/catalog
GET  /model-control/v1/tasks
GET  /model-control/v1/tasks/{task_id}
POST /model-control/v1/download
POST /model-control/v1/remove
```

Download request:

```json
{
  "artifact_id": "h3.fl2va.trunk.int8-convrot",
  "expected_sha256": "e889202c41dafb67b10d67b97f0d8541508036a6090af23425a5c2615d03c47a",
  "confirm": "download:h3.fl2va.trunk.int8-convrot"
}
```

Removal uses the same digest guard and
`"confirm": "remove:<artifact_id>"`. The mutation returns a task immediately;
poll its exact task id. A `success` task means the bytes on disk are verified,
not that a workflow has executed or passed visual review.

## Runtime boundary

Model Control does not restart ComfyUI or unload models. Install the extension
through the normal public-repository path, restart ComfyUI once, then operate
its bounded API. Loader inventory should be refreshed after each completed
download and before a graph is submitted.
