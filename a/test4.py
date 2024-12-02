import cv2
from ultralytics import YOLO

# YOLOv8 modelini yükle
model = YOLO('yolov8n.pt')

# Kamerayı başlat
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # YOLOv8 ile algılama yap
    results = model(frame)

    # Algılama sonuçlarını çizin
    annotated_frame = results[0].plot()

    # Sonuçları göster
    cv2.imshow('YOLOv8 Algılama', annotated_frame)
    
    # 'q' tuşuna basarak çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamera ve pencereleri serbest bırak
cap.release()
cv2.destroyAllWindows()
