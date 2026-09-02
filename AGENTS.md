# ComfyUI Model Control runbook

This repository is a narrow model-lifecycle extension for one remote ComfyUI
runtime. It is not a model manager, shell, creative node pack, or arbitrary
filesystem API.

## Invariants

- Only artifacts declared in the source-controlled catalog may be downloaded
  or removed.
- Every artifact has an exact HTTPS URL, byte count, SHA-256 digest, Comfy
  folder category, and filename.
- Never accept a caller-supplied URL, destination directory, filename, shell
  command, Git ref, Python package, or executable.
- Resolve every registered destination through ComfyUI `folder_paths`; refuse
  path traversal and symlink targets. Never assume the first root is the only
  root visible to loaders.
- Download to a `.part` file, support byte-range resume, verify size and digest,
  then atomically replace the final path.
- Keep only one mutation task active at a time and expose bounded progress.
- Refuse removal unless every discovered copy has the exact allowlisted size
  and digest; validate all copies before deleting any copy.
- Never modify ComfyUI core, custom nodes, Python, PyTorch, CUDA, drivers,
  workflows, inputs, outputs, or the physical host.
- A successful download changes disk state only. Restart/reload and workflow
  validation remain separate operations.

## Verification

```bash
python3 -m compileall -q .
python3 -m unittest discover -s tests -v
git diff --check
```
