#!/usr/bin/bash
# Populates resources/ (gitignored — see RESOURCES.md) with the model weights,
# compiled HEFs, and TTS voices this project needs. Safe to re-run; existing
# files are skipped unless -f is passed.
#
# Sources are the same URLs already used by this repo's per-demo
# scripts/python/*/download_resources.sh files (Hailo model zoo / hailo-csdata S3),
# plus the public HuggingFace/GitHub/ONNX model zoo hosts for TTS and vision models.

set -e
cd "$(dirname "$0")/resources"

FORCE=0
[ "$1" = "-f" ] && FORCE=1

fetch() {
  local url="$1" dest="$2"
  if [ -f "$dest" ] && [ "$FORCE" -eq 0 ]; then
    echo "skip (exists): $dest"
    return
  fi
  mkdir -p "$(dirname "$dest")"
  echo "downloading: $dest"
  wget -q --show-progress -O "$dest" "$url"
}

echo "=== Whisper HEFs (speech_recognition) ==="
fetch "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/hefs/h8/tiny-whisper-decoder-fixed-sequence-matmul-split.hef" "hefs/h8/tiny/tiny-whisper-decoder-fixed-sequence-matmul-split.hef"
fetch "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/hefs/h8/tiny-whisper-encoder-10s_15dB.hef" "hefs/h8/tiny/tiny-whisper-encoder-10s_15dB.hef"
fetch "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/hefs/h8l_rpi/tiny-whisper-decoder-fixed-sequence-matmul-split_h8l.hef" "hefs/h8l/tiny/tiny-whisper-decoder-fixed-sequence-matmul-split_h8l.hef"
fetch "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/hefs/h8l_rpi/tiny-whisper-encoder-10s_15dB_h8l.hef" "hefs/h8l/tiny/tiny-whisper-encoder-10s_15dB_h8l.hef"
fetch "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/hefs/h8/base-whisper-decoder-fixed-sequence-matmul-split.hef" "hefs/h8/base/base-whisper-decoder-fixed-sequence-matmul-split.hef"
fetch "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/hefs/h8/base-whisper-encoder-5s.hef" "hefs/h8/base/base-whisper-encoder-5s.hef"
fetch "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/hefs/h8l_rpi/base-whisper-decoder-fixed-sequence-matmul-split_h8l.hef" "hefs/h8l/base/base-whisper-decoder-fixed-sequence-matmul-split_h8l.hef"
fetch "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/hefs/h8l_rpi/base-whisper-encoder-5s_h8l.hef" "hefs/h8l/base/base-whisper-encoder-5s_h8l.hef"

echo "=== Whisper decoder tokenization assets ==="
fetch "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/npy%20files/whisper/decoder_assets/tiny/decoder_tokenization/onnx_add_input_tiny.npy" "decoder_assets/tiny/decoder_tokenization/onnx_add_input_tiny.npy"
fetch "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/npy%20files/whisper/decoder_assets/tiny/decoder_tokenization/token_embedding_weight_tiny.npy" "decoder_assets/tiny/decoder_tokenization/token_embedding_weight_tiny.npy"
fetch "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/npy%20files/whisper/decoder_assets/base/decoder_tokenization/onnx_add_input_base.npy" "decoder_assets/base/decoder_tokenization/onnx_add_input_base.npy"
fetch "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/npy%20files/whisper/decoder_assets/base/decoder_tokenization/token_embedding_weight_base.npy" "decoder_assets/base/decoder_tokenization/token_embedding_weight_base.npy"

echo "=== Other Hailo HEFs (object/pose/segmentation/lane/super-res) ==="
fetch "https://hailo-model-zoo.s3.eu-west-2.amazonaws.com/ModelZoo/Compiled/v2.15.0/hailo8/yolov8n.hef" "hefs/yolov8n.hef"
fetch "https://hailo-model-zoo.s3.eu-west-2.amazonaws.com/ModelZoo/Compiled/v2.12.0/hailo8/yolov8s_pose.hef" "hefs/yolov8s_pose.hef"
fetch "https://hailo-model-zoo.s3.eu-west-2.amazonaws.com/ModelZoo/Compiled/v2.15.0/hailo8/yolov5m_seg.hef" "hefs/yolov5m_seg.hef"
fetch "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/hefs/h8/yolov5m_seg_with_nms.hef" "hefs/yolov5m_seg_with_nms.hef"
fetch "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/hefs/h8/yolov8s_seg.hef" "hefs/yolov8s_seg.hef"
fetch "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/hefs/h8/fast_sam_s.hef" "hefs/fast_sam_s.hef"
fetch "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/hefs/h8/ufld_v2_tu.hef" "hefs/ufld_v2_tu.hef"
fetch "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/hefs/h8/real_esrgan_x2.hef" "hefs/real_esrgan_x2.hef"

echo "=== ONNX model zoo ==="
fetch "https://github.com/onnx/models/raw/main/validated/vision/body_analysis/emotion_ferplus/model/emotion-ferplus-8.onnx" "onnx/emotion-ferplus-8.onnx"

echo "=== Piper TTS voices (rhasspy/piper-voices) ==="
fetch "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx" "tts/en_US-lessac-medium.onnx"
fetch "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json" "tts/en_US-lessac-medium.onnx.json"
fetch "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/hfc_female/medium/en_US-hfc_female-medium.onnx" "tts/en_US-hfc_female-medium.onnx"
fetch "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/hfc_female/medium/en_US-hfc_female-medium.onnx.json" "tts/en_US-hfc_female-medium.onnx.json"

echo "=== Piper runtime (linux aarch64) ==="
fetch "https://github.com/rhasspy/piper/releases/latest/download/piper_linux_aarch64.tar.gz" "piper/piper_linux_aarch64.tar.gz"

echo "=== Whisper checkpoints (base.pt / tiny.pt) ==="
if [ -f "models/whisper-base/base.pt" ] && [ -f "models/whisper-base/tiny.pt" ] && [ "$FORCE" -eq 0 ]; then
  echo "skip (exists): models/whisper-base/{base,tiny}.pt"
else
  echo "fetching via the openai-whisper package's own downloader (verifies checksums)..."
  mkdir -p models/whisper-base
  python3 -c "
import whisper, shutil
for name in ('base', 'tiny'):
    path = whisper._download(whisper._MODELS[name], 'models/whisper-base', False)
    shutil.move(path, f'models/whisper-base/{name}.pt')
"
fi

echo "=== ONNX / TFLite / YOLO checkpoints not auto-fetched ==="
echo "resources/models/tensorflow/*.tflite, resources/models/yolo11n.pt, resources/assets/mel_filters.npz"
echo "and resources/hefs/h8l/face_emotion/lightface_slim.hef are small (<15MB each) and untracked/local;"
echo "keep your own copies or re-source them if missing."

cat <<'EOF'

=== Manual step required: HailoRT ===
resources/hailort/hailort_4.21.0_arm64.deb and
resources/hailort/hailort-4.21.0-cp311-cp311-linux_aarch64.whl are NOT
auto-downloaded — Hailo requires a free developer-zone account + EULA
acceptance. See RESOURCES.md for the manual download step.

=== Manual step (optional): DeGirum PySDK zoo models ===
resources/models/yolov8n_coco--640x640_quant_hailort_multidevice_1/ and the
yolov8n_relu6_* variants are cached automatically by degirum PySDK on first
use (zoo_url="https://hub.degirum.com/degirum/hailo"). No action needed
unless you want to pre-warm the cache.
EOF
