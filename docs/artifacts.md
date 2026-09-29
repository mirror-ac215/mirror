# Artifacts

What we store in the team bucket `gs://mirror-ac215-data/`, where each file came from, and how good it is.

| File (GCS path) | What it is | Size | Source | Metrics |
|---|---|---|---|---|
| `models/cv/inherited-v3/vit_b16_v3_best.pth` | ViT-B/16, 7-class facial expression, main model | 327 MB | CSCI E-25, `facial_emotion_recognition_v3_Mostafa_Galal.ipynb` | test: 66.6% top-1, 83.8% top-2, 0.645 macro-F1 |
| `models/cv/inherited-v3/efficientnet_b0_v3.pth` | EfficientNet-B0, backup / lighter CV model | 16 MB | same notebook | test: 65.2% top-1, 0.626 macro-F1 |
| `models/cv/inherited-v3/mobilenet_v3_large_best.pth` | MobileNetV3-Large, lightest CV model | 16 MB | CSCI E-25, `01_model_training_and_evaluation.ipynb` | best validation accuracy 60.6% |
| `models/cv/inherited-v3/per_class_thresholds.npy` | Per-class decision thresholds for the CV models | <1 KB | v3 notebook | n/a |
| `models/llm/adapter-v1/` | QLoRA adapter on `Qwen/Qwen2.5-3B-Instruct` (r=32, alpha=64, dropout 0.05, all attention and MLP layers) | 240 MB | CSCI E-222, `Jordan_Peterson_Clone.ipynb` (masked, best checkpoint) | to be evaluated in MS3/MS4 |
| `data/raw/fer2013/archive.zip` | FER-2013 dataset | 60 MB | public (Kaggle) | 7 classes, 48x48 grayscale |
| `data/raw/persona/*.csv` | Persona prompt/response pairs | <1 MB | extracted from public long-form interviews | 380 pairs: 304 train / 38 val / 38 test |

Everything lives in `gs://mirror-ac215-data/`. Download with `gcloud storage cp gs://mirror-ac215-data/<path> .` (requires project access).
