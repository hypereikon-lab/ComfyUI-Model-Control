from __future__ import annotations

from aiohttp import web

from .model_control import ModelControl, ModelControlError

WEB_DIRECTORY = None
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

CONTROL = ModelControl.for_comfy()


try:
    from server import PromptServer

    routes = PromptServer.instance.routes

    @routes.get("/model-control/v1/capabilities")
    async def model_control_capabilities(_request):
        return web.json_response(CONTROL.capabilities())

    @routes.get("/model-control/v1/catalog")
    async def model_control_catalog(_request):
        return web.json_response(CONTROL.catalog())

    @routes.get("/model-control/v1/tasks")
    async def model_control_tasks(_request):
        return web.json_response(CONTROL.tasks())

    @routes.get("/model-control/v1/tasks/{task_id}")
    async def model_control_task(request):
        try:
            return web.json_response(CONTROL.task(request.match_info["task_id"]))
        except ModelControlError as exc:
            return web.json_response({"error": str(exc)}, status=404)

    async def _mutation(request, action: str):
        if request.content_type != "application/json":
            return web.json_response({"error": "application/json required"}, status=415)
        try:
            data = await request.json()
            required = {"artifact_id", "expected_sha256", "confirm"}
            if set(data) != required:
                raise ModelControlError("request must contain exactly artifact_id, expected_sha256, confirm")
            if action == "download":
                result = CONTROL.start_download(**data)
            else:
                result = CONTROL.start_remove(**data)
            return web.json_response(result, status=202)
        except ModelControlError as exc:
            return web.json_response({"error": str(exc)}, status=409)
        except Exception:
            return web.json_response({"error": "invalid JSON request"}, status=400)

    @routes.post("/model-control/v1/download")
    async def model_control_download(request):
        return await _mutation(request, "download")

    @routes.post("/model-control/v1/remove")
    async def model_control_remove(request):
        return await _mutation(request, "remove")

except ImportError:
    # Allows the bounded implementation to be unit-tested outside ComfyUI.
    pass


__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
