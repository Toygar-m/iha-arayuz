import torch
if torch.cuda.is_available():
    device = torch.device("cuda")  # GPU kullanılabilir
    print("GPU is available.")
else:
    device = torch.device("cpu")  # GPU kullanılabilir değilse CPU kullan
    print("GPU is not available, using CPU.")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
print(f"Number of GPUs available: {torch.cuda.device_count()}")
from ultralytics import YOLO
import torch

# CUDA kullanılabilirliğini kontrol et
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# YOLO modelini yükleyin ve cihazınıza taşıyın
model = YOLO('yolo11n-seg.pt').to(device)

# Modeli kullanmaya başla
print(f"Model is running on {device}")
