import torch

# CUDA'nın kullanılabilir olup olmadığını kontrol et
cuda_available = torch.cuda.is_available()
print(f"CUDA mevcut mu: {cuda_available}")

# Eğer CUDA mevcutsa, GPU'nun özelliklerini yazdır
if cuda_available:
    print(f"CUDA cihaz adı: {torch.cuda.get_device_name(0)}")
    print(f"CUDA cihaz belleği (MB): {torch.cuda.get_device_properties(0).total_memory // 1024**2}")
else:
    print("CUDA cihazı bulunamadı.")
