from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ModelArtifact:
    artifact_id: str
    family: str
    role: str
    folder_category: str
    filename: str
    url: str
    size_bytes: int
    sha256: str
    source_revision: str
    downloadable: bool = True
    removable: bool = True

    def public_dict(self) -> dict:
        return asdict(self)


COMFY_H3_REVISION = "4cc1d817b6184899b41293954329f576cb5ae86b"
PDD_REVISION = "f4cac997f880e93cf6940af61ee8d58ef31ff7f3"
FUN_CONTROL_REVISION = "c79bdb788d0f77460c3952a4c1ae3b3b7d71a4c8"
SAM3_REVISION = "f38cd62b71494b53ac2b56ca36e24f3c8d565581"
DA3_REVISION = "248c0c2c1fca3cf3046db1d0d3d5256f2d078f41"
SDPOSE_REVISION = "f122ac7976997885e3bfeab2bb3a537a6bc250bc"
REF_TURBO8_REVISION = "0eebcc7e79f9cb200927c80b8e7595265b770e34"
PDMD_REVISION = "c41575a27fe1e7d7dcc4630e6cc410130dcbba53"
DMAD_REVISION = "1db9d50082f491fb5b2fbbee7499fb93e9190c51"
H3_VAE_INT8_REVISION = "d8023be02fefbb3633b0cd335c3879f91177299d"


def _hf(repo: str, revision: str, path: str) -> str:
    return f"https://huggingface.co/{repo}/resolve/{revision}/{path}?download=true"


CATALOG = {
    item.artifact_id: item
    for item in [
        ModelArtifact(
            "h3.video-vae.int8-convrot", "h3-experimental", "video-vae", "vae",
            "minimax_h3_video_vae_int8_convrot.safetensors",
            _hf("Kijai/MiniMax-H3-experimental", H3_VAE_INT8_REVISION,
                "minimax_h3_video_vae_int8_convrot.safetensors"),
            3_171_670_912,
            "9bb2d96f218c76babd85e0611b85ca8fb330a90546c01a0005e8a58a59593410",
            H3_VAE_INT8_REVISION,
        ),
        ModelArtifact(
            "h3.ref2va.turbo-8-v1-768p", "ref2va", "accelerator-lora", "loras",
            "minimax_h3_ref2v_turbo_8step_v1.0_768p_comfyui_bf16.safetensors",
            _hf("lightx2v/Minimax-h3-Turbo", REF_TURBO8_REVISION,
                "minimax_h3_ref2v_turbo_8step_v1.0_768p_comfyui_bf16.safetensors"),
            1_956_193_000,
            "6a56f41ab4229c9dd845b9501bbd475ee57e112d846cf2e819d534a1ae928c5a",
            REF_TURBO8_REVISION,
        ),
        ModelArtifact(
            "h3.pdmd-4-rank57", "h3-experimental", "accelerator-lora", "loras",
            "minimax_h3_pdmd_4step_lora_avg_rank_57_bf16.safetensors",
            _hf("Kijai/MiniMax-H3-experimental", PDMD_REVISION,
                "loras/minimax_h3_pdmd_4step_lora_avg_rank_57_bf16.safetensors"),
            558_735_392,
            "b5c62eb228a4f604890566ad698713703ed221302e0df1c067725c39f11efc37",
            PDMD_REVISION,
        ),
        ModelArtifact(
            "h3.dmad-4-rank39", "h3-experimental", "accelerator-lora", "loras",
            "minimax_h3_DMAD_4step_full_lora_avg_rank_39_bf16.safetensors",
            _hf("Kijai/MiniMax-H3-experimental", DMAD_REVISION,
                "loras/minimax_h3_DMAD_4step_full_lora_avg_rank_39_bf16.safetensors"),
            366_647_000,
            "ddfdd94f4c9a0f32bf3649bb8e98ca20db572e4db6bcd9cca546a5b33ea32d11",
            DMAD_REVISION,
        ),
        ModelArtifact(
            "h3.fl2va.trunk.int8-convrot",
            "fl2va",
            "quality-trunk",
            "diffusion_models",
            "minimax_h3_fl2va_pruned_int8_convrot.safetensors",
            _hf(
                "Comfy-Org/MiniMax-H3",
                COMFY_H3_REVISION,
                "diffusion_models/minimax_h3_fl2va_pruned_int8_convrot.safetensors",
            ),
            20_970_379_616,
            "e889202c41dafb67b10d67b97f0d8541508036a6090af23425a5c2615d03c47a",
            COMFY_H3_REVISION,
        ),
        ModelArtifact(
            "h3.ref2va.trunk.int8-convrot",
            "ref2va",
            "quality-trunk",
            "diffusion_models",
            "minimax_h3_ref2va_pruned_int8_convrot.safetensors",
            _hf(
                "Comfy-Org/MiniMax-H3",
                COMFY_H3_REVISION,
                "diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors",
            ),
            20_970_379_616,
            "9255f52b6677845ad238f20dfaafa94727053694127ab7f255c048f0f9365779",
            COMFY_H3_REVISION,
        ),
        ModelArtifact(
            "h3.fl2va.turbo-8",
            "fl2va",
            "accelerator-lora",
            "loras",
            "minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors",
            _hf(
                "Comfy-Org/MiniMax-H3",
                COMFY_H3_REVISION,
                "loras/minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors",
            ),
            1_956_193_000,
            "2339acdf19bfe123f46b971ea35d367a84adb85de43627e1eceafa5a5b2b111e",
            COMFY_H3_REVISION,
        ),
        ModelArtifact(
            "h3.fl2va.turbo-4",
            "fl2va",
            "accelerator-lora",
            "loras",
            "minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors",
            _hf(
                "Comfy-Org/MiniMax-H3",
                COMFY_H3_REVISION,
                "loras/minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors",
            ),
            1_956_192_992,
            "c396a9a06f58399e9df9754b18299818d84a2ddd371724ba48fe4a41221437dc",
            COMFY_H3_REVISION,
        ),
        ModelArtifact(
            "h3.ref2va.turbo-4",
            "ref2va",
            "accelerator-lora",
            "loras",
            "minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors",
            _hf(
                "Comfy-Org/MiniMax-H3",
                COMFY_H3_REVISION,
                "loras/minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors",
            ),
            1_956_193_000,
            "5b9ab5ade15d0775676d01a907268a69a1468dc6033b3b0d3ded5502f3ebb84c",
            COMFY_H3_REVISION,
        ),
        ModelArtifact(
            "h3.fl2va.pdd-8",
            "fl2va",
            "accelerator-pdd-lora",
            "loras",
            "MiniMax-H3-FL2VA-Acc-8Step_pruned_comfy.safetensors",
            _hf(
                "Kijai/MiniMax-H3-experimental",
                PDD_REVISION,
                "loras/MiniMax-H3-FL2VA-Acc-8Step_pruned_comfy.safetensors",
            ),
            1_725_921_392,
            "e97b813a6f857b9dab310f31ec30a8334f63a3e7dcb5d07c0c91933d3447a897",
            PDD_REVISION,
        ),
        ModelArtifact(
            "h3.ref2va.pdd-8",
            "ref2va",
            "accelerator-pdd-lora",
            "loras",
            "MiniMax-H3-Ref2VA-Acc-8Step_pruned_comfy.safetensors",
            _hf(
                "Kijai/MiniMax-H3-experimental",
                PDD_REVISION,
                "loras/MiniMax-H3-Ref2VA-Acc-8Step_pruned_comfy.safetensors",
            ),
            1_725_921_392,
            "6f18e1c2eccb14b37322607730f26b16bf1169b56cd098ea006cffaec43d1e39",
            PDD_REVISION,
        ),
        ModelArtifact(
            "h3.fun-control.union",
            "h3-control",
            "model-patch",
            "model_patches",
            "minimax_h3_fun_controlnet_union_pruned_int8_convrot.safetensors",
            _hf(
                "Kijai/MiniMax-H3-experimental",
                FUN_CONTROL_REVISION,
                "controlnet/minimax_h3_fun_controlnet_union_pruned_int8_convrot.safetensors",
            ),
            2_296_635_360,
            "9c645c0a308c8af361efd43b409710f6f8fec0db297c29503e141a84991fed0c",
            FUN_CONTROL_REVISION,
        ),
        ModelArtifact(
            "perception.sam3.1.multiplex-fp16",
            "sam3",
            "tracked-mask-model",
            "checkpoints",
            "sam3.1_multiplex_fp16.safetensors",
            _hf(
                "Comfy-Org/sam3.1",
                SAM3_REVISION,
                "checkpoints/sam3.1_multiplex_fp16.safetensors",
            ),
            1_745_546_848,
            "9ba99c92703c2e8b4f47de2d34a539bb8e18923049e238b780d70dbe6368eb03",
            SAM3_REVISION,
        ),
        ModelArtifact(
            "perception.da3.mono-large",
            "depth-anything-3",
            "depth-control-model",
            "geometry_estimation",
            "depth_anything_3_mono_large.safetensors",
            _hf(
                "Comfy-Org/Depth-Anything-3",
                DA3_REVISION,
                "geometry_estimation/depth_anything_3_mono_large.safetensors",
            ),
            1_336_748_056,
            "9b44eda5bedba5b4e125686fdb79d1db309c1b9785277576eb930f885b008f96",
            DA3_REVISION,
        ),
        ModelArtifact(
            "perception.sdpose.wholebody-fp16",
            "sdpose",
            "pose-control-model",
            "checkpoints",
            "sdpose_wholebody_fp16.safetensors",
            _hf(
                "Comfy-Org/SDPose",
                SDPOSE_REVISION,
                "checkpoints/sdpose_wholebody_fp16.safetensors",
            ),
            1_916_645_792,
            "63d01f9a7494560693b24767f4469d59c9d3266b31ff0a253e74d1e611442721",
            SDPOSE_REVISION,
        ),
        ModelArtifact(
            "perception.sdpose.detector-fp16",
            "sdpose",
            "pose-detector-model",
            "diffusion_models",
            "rt_detr_v4-x-hgnet_fp16.safetensors",
            _hf(
                "Comfy-Org/SDPose",
                SDPOSE_REVISION,
                "diffusion_models/rt_detr_v4-x-hgnet_fp16.safetensors",
            ),
            123_968_978,
            "581f9af9bbabb664d1891cbccd823308b176ecd409146f954dfa39af3bec2476",
            SDPOSE_REVISION,
        ),
        ModelArtifact(
            "h3.fl2va.trunk.fp8-scaled-legacy",
            "fl2va",
            "retirement-only",
            "diffusion_models",
            "minimax_h3_fl2va_pruned_fp8_scaled.safetensors",
            _hf(
                "Comfy-Org/MiniMax-H3",
                COMFY_H3_REVISION,
                "diffusion_models/minimax_h3_fl2va_pruned_fp8_scaled.safetensors",
            ),
            20_958_205_608,
            "12944c1f7791637e7de12208aef04da82bd26b95271b1b47d817364315ade993",
            COMFY_H3_REVISION,
            downloadable=False,
            removable=True,
        ),
        ModelArtifact(
            "h3.ref2va.trunk.fp8-scaled-legacy",
            "ref2va",
            "retirement-only",
            "diffusion_models",
            "minimax_h3_ref2va_pruned_fp8_scaled.safetensors",
            _hf(
                "Comfy-Org/MiniMax-H3",
                COMFY_H3_REVISION,
                "diffusion_models/minimax_h3_ref2va_pruned_fp8_scaled.safetensors",
            ),
            20_958_205_608,
            "f86f2f79ebd2d76eb8eeb46091e83982e6ff51d255747e7b16e92834b392b8e9",
            COMFY_H3_REVISION,
            downloadable=False,
            removable=True,
        ),
    ]
}
