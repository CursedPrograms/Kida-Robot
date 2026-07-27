# resources/

Model weights, compiled HEFs, TTS voices, and vendor runtime packages used by
KIDA. The whole folder is gitignored (`/resources/` in `.gitignore`) — it's
populated locally, not committed.

```
assets/            whisper mel filterbank
decoder_assets/    whisper decoder tokenization tensors (tiny/base)
hailort/           HailoRT .deb/.whl — manual download, see below
hefs/              compiled Hailo HEF models (object detection, pose, segmentation, whisper, ...)
models/            .pt / .tflite checkpoints, plus DeGirum PySDK zoo cache dirs
onnx/              standalone ONNX models
piper/             Piper TTS runtime tarball
tts/               Piper TTS voice models (.onnx)
```

## Setting up

```
./download_resources.sh
```

Pulls the whisper HEFs/checkpoints/decoder assets, the Hailo model-zoo HEFs
(object detection, pose, segmentation, lane detection, super resolution),
the two Piper TTS voices, the Piper runtime tarball, and the ONNX emotion
model — all from their original public sources (Hailo's model CDN,
HuggingFace, GitHub releases, the ONNX model zoo). Re-running skips files
that already exist; pass `-f` to force re-download.

## Manual step: HailoRT

`resources/hailort/hailort_4.21.0_arm64.deb` and
`resources/hailort/hailort-4.21.0-cp311-cp311-linux_aarch64.whl` can't be
scripted — Hailo requires a free developer-zone account and EULA acceptance:

1. Sign in at https://hailo.ai/developer-zone/
2. Download HailoRT 4.21.0 for your platform (the `.deb` for apt, the `.whl`
   for Python 3.11) and place both in `resources/hailort/`.
3. Install:
   ```
   sudo apt install ./resources/hailort/hailort_4.21.0_arm64.deb
   pip install ./resources/hailort/hailort-4.21.0-cp311-cp311-linux_aarch64.whl
   ```

## DeGirum PySDK zoo models

`resources/models/yolov8n_coco--640x640_quant_hailort_multidevice_1/` and the
`yolov8n_relu6_*` variants are cached automatically by degirum PySDK on
first use (`zoo_url="https://hub.degirum.com/degirum/hailo"`) — no action
needed.
