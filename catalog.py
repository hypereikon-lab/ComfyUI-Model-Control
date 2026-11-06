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
FASTH3_TRIM_REVISION = "f66c13dc17391dd4da99242a407918b92bf7d5fc"
FL2VA_TURBO_PREVIEW_REVISION = "587e806edadec7b92393556b3ac3115cadfb32be"
FL2VA_TURBO_OCTOBER_REVISION = "30f485ed874aa44c8183348ad361c5eabad318da"
PIKA_FLEX_REVISION = "3ff166447d5edb1406107ab8370c42000ce173e4"


def _hf(repo: str, revision: str, path: str) -> str:
    return f"https://huggingface.co/{repo}/resolve/{revision}/{path}?download=true"


CATALOG = {
    item.artifact_id: item
    for item in [
        ModelArtifact(
            "h3.ref2va.original-bf16-ptd", "ref2va", "original-base", "diffusion_models",
            "minimax_h3_ref2va_bf16.safetensors",
            _hf("Comfy-Org/MiniMax-H3", "54472221d27c695fca9621b0c3ed52f06c4af707",
                "diffusion_models/minimax_h3_ref2va_bf16.safetensors"),
            66_280_487_368,
            "e32c54c1a7b4f5f397f195cea267ccb18806303bb665678c4bee60953bdf3026",
            "54472221d27c695fca9621b0c3ed52f06c4af707",
        ),
        ModelArtifact(
            "h3.ref2va.ptd-refasymopd-8step", "ref2va", "ptd-adapter-bank", "ptd",
            "MiniMax-H3-Ref2VA-PTD-RefAsymOPD-8Step.safetensors",
            _hf("taobao-content-ai/MiniMax-H3-PTD-RefAsymOPD-LoRAs", "d1f88c89c352e7751b56b5f32c7b657fb3e0f2c5",
                "MiniMax-H3-Ref2VA-PTD-RefAsymOPD-8Step.safetensors"),
            11_112_893_024,
            "6796802b9150110a3cd7f66891c9e6190502a432c30b0fa1aa299724cfc15cc3",
            "d1f88c89c352e7751b56b5f32c7b657fb3e0f2c5",
        ),
        ModelArtifact(
            "h3.ref2va.turbo-4-v10-768p", "ref2va", "accelerator-lora", "loras",
            "minimax_h3_ref2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors",
            _hf("lightx2v/Minimax-h3-Turbo", FL2VA_TURBO_OCTOBER_REVISION,
                "minimax_h3_ref2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors"),
            1_956_193_000,
            "b4da466e43588004097dfbcde245ccc439c34a26bc997cb76a0b53a1d549ea0d",
            FL2VA_TURBO_OCTOBER_REVISION,
        ),
        ModelArtifact(
            "h3.fl2va.turbo-4-v01", "fl2va", "accelerator-lora", "loras",
            "minimax_h3_fl2v_lightx2v_turbo_4step_v0.1_comfy.safetensors",
            _hf("Kijai/MiniMax-H3_comfy", FL2VA_TURBO_PREVIEW_REVISION,
                "loras/minimax_h3_fl2v_lightx2v_turbo_4step_v0.1_comfy.safetensors"),
            1_956_171_984,
            "fc9b6500f0331fe925b004738baaa31bd34104741c8bf9334816f9ac3005c8c1",
            FL2VA_TURBO_PREVIEW_REVISION,
        ),
        ModelArtifact(
            "h3.fl2va.turbo-4-v13", "fl2va", "accelerator-lora", "loras",
            "minimax_h3_fl2v_turbo_4step_v1.3_768p_comfyui_bf16.safetensors",
            _hf("lightx2v/Minimax-h3-Turbo", FL2VA_TURBO_OCTOBER_REVISION,
                "minimax_h3_fl2v_turbo_4step_v1.3_768p_comfyui_bf16.safetensors"),
            1_956_193_000,
            "70103fd0d80a947ed4e7fe6f88915863d54ef22c5cab03bd5d2fd649385ffe1e",
            FL2VA_TURBO_OCTOBER_REVISION,
        ),
        ModelArtifact(
            "h3.fl2va.turbo-8-v11", "fl2va", "accelerator-lora", "loras",
            "minimax_h3_fl2v_turbo_8step_v1.1_768p_comfyui_bf16.safetensors",
            _hf("lightx2v/Minimax-h3-Turbo", FL2VA_TURBO_OCTOBER_REVISION,
                "minimax_h3_fl2v_turbo_8step_v1.1_768p_comfyui_bf16.safetensors"),
            1_956_193_000,
            "fb4c00361c94bad47f878d5e096c6cab2f45063b0968bd5756dcb7da6936f53e",
            FL2VA_TURBO_OCTOBER_REVISION,
        ),
        ModelArtifact(
            "h3.fl2va.pika-flex", "fl2va", "post-trained-lora", "loras",
            "pika_h3_flex_fl2va_comfy_bf16.safetensors",
            _hf("Pika-Labs/Pika-H3-Flex", PIKA_FLEX_REVISION,
                "comfy/loras/pika_h3_flex_fl2va_comfy_bf16.safetensors"),
            1_956_172_176,
            "68783e6447696ec365d13c0554941e070bee4cfea13c37da52498ec4f9a53f89",
            PIKA_FLEX_REVISION,
        ),
        ModelArtifact(
            "h3.fasth3.trim-8.nvfp4", "t2av", "experimental-distilled-trunk", "diffusion_models",
            "fastvideo_fasth3_trim_8step_nvfp4.safetensors",
            _hf("FastVideo/FastVideo-FastH3-Trim-Comfy", FASTH3_TRIM_REVISION,
                "diffusion_models/fastvideo_fasth3_trim_8step_nvfp4.safetensors"),
            11_894_623_166,
            "748b2bcc9c4b7bf7b23406987b42d4ac40362070c164cf11092482be6a863455",
            FASTH3_TRIM_REVISION,
        ),
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
        ModelArtifact(
            "h3.community.native-spatial-upscaler",
            "h3-open-community",
            "latent-upscaler",
            "latent_upscale_models",
            "minimax_h3_latent_upscaler_3d_conv_v1_fp16.safetensors",
            _hf(
                "LBH-123-AI/Minimax_h3_latent_Upscaler",
                "3f941d5d182014dd5c0a5e16330420ee2d4aa0c6",
                "minimax_h3_latent_upscaler_3d_conv_v1/minimax_h3_latent_upscaler_3d_conv_v1_fp16.safetensors",
            ),
            690_592_672,
            "043e5a48e161610ef6c3ea974645220354d06fa618abca15f76d084812eb55c2",
            "3f941d5d182014dd5c0a5e16330420ee2d4aa0c6",
        ),
        ModelArtifact(
            "h3.community.pika-ref2va-v1",
            "h3-open-community",
            "conditioning-lora",
            "loras",
            "pika_h3_flex_ref2va_v1_bf16.safetensors",
            _hf(
                "Comfy-Org/MiniMax-H3",
                "54472221d27c695fca9621b0c3ed52f06c4af707",
                "loras/pika_h3_flex_ref2va_v1_bf16.safetensors",
            ),
            1_956_172_304,
            "de3745ceb7d8d5c20898dd8fa3a05f1c0b00089ccd55297b2a8bab95c766b0e0",
            "54472221d27c695fca9621b0c3ed52f06c4af707",
        ),
        ModelArtifact(
            "h3.community.open-rank16",
            "h3-open-community",
            "refiner-lora",
            "loras",
            "minimax_h3_open_regenerate_2k_refiner_rank_16_bf16.safetensors",
            _hf(
                "Kijai/MiniMax-H3-experimental",
                "f5c3b1d5a63e008a691fca1b6096fd57a5307536",
                "loras/minimax_h3_open_regenerate_2k_refiner_rank_16_bf16.safetensors",
            ),
            155_133_472,
            "add559cd92e2b17b42ac080516b476df120903e485fc98add4538e0217820fbd",
            "f5c3b1d5a63e008a691fca1b6096fd57a5307536",
        ),
        ModelArtifact(
            "h3.community.lms-sharp-r64",
            "h3-open-community",
            "detail-lora",
            "loras",
            "minimax_h3_lms_v1.0_r64.safetensors",
            _hf(
                "Alissonerdx/Minimax-H3-ComfyUI",
                "43a8d127ecb0418017c6742d348416ef39533b1e",
                "loras/minimax_h3_lms_v1.0_r64.safetensors",
            ),
            1_239_664_536,
            "16f3195bc6bffa431c0598dc2031e520ba058b4fcbc9f104db9e3fdfdeacf60c",
            "43a8d127ecb0418017c6742d348416ef39533b1e",
        ),
        ModelArtifact(
            "h3.community.video-vae",
            "h3-open-community",
            "video-vae",
            "vae",
            "minimax_h3_video_vae_int8_convrot_comfy_org.safetensors",
            _hf(
                "Comfy-Org/MiniMax-H3",
                "54472221d27c695fca9621b0c3ed52f06c4af707",
                "vae/minimax_h3_video_vae_int8_convrot.safetensors",
            ),
            2_811_065_184,
            "52a2c8c73583c86e4f41cdcce3a6ad0ea562987bc0bf3d60a0cef5f5c8e60c0e",
            "54472221d27c695fca9621b0c3ed52f06c4af707",
        ),
    ]
}
