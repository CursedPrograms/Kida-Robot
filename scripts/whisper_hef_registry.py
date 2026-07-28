import os

# Repo root is one level up from scripts/ — resolved from this file's own
# location so callers work regardless of CWD (this registry used to hardcode
# "scripts/resources/hefs/..." which never existed; the real files live at
# <repo root>/resources/hefs/...).
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_HEFS_DIR  = os.path.join(_REPO_ROOT, "resources", "hefs")

HEF_REGISTRY = {
    "base": {
        "hailo8": {
            "encoder": os.path.join(_HEFS_DIR, "h8", "base", "base-whisper-encoder-5s.hef"),
            "decoder": os.path.join(_HEFS_DIR, "h8", "base", "base-whisper-decoder-fixed-sequence-matmul-split.hef"),
        },
        "hailo8l": {
            "encoder": os.path.join(_HEFS_DIR, "h8l", "base", "base-whisper-encoder-5s_h8l.hef"),
            "decoder": os.path.join(_HEFS_DIR, "h8l", "base", "base-whisper-decoder-fixed-sequence-matmul-split_h8l.hef"),
        }
    },
    "tiny": {
        "hailo8": {
            "encoder": os.path.join(_HEFS_DIR, "h8", "tiny", "tiny-whisper-encoder-10s_15dB.hef"),
            "decoder": os.path.join(_HEFS_DIR, "h8", "tiny", "tiny-whisper-decoder-fixed-sequence-matmul-split.hef"),
        },
        "hailo8l": {
            "encoder": os.path.join(_HEFS_DIR, "h8l", "tiny", "tiny-whisper-encoder-10s_15dB_h8l.hef"),
            "decoder": os.path.join(_HEFS_DIR, "h8l", "tiny", "tiny-whisper-decoder-fixed-sequence-matmul-split_h8l.hef"),
        }
    }
}