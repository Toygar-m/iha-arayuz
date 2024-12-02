import cv2

def list_available_cameras():
    index = 0
    available_cameras = []
    while True:
        # Kamera bağlantısını test et
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            break
        else:
            available_cameras.append(index)
            cap.release()
        index += 1
    
    return available_cameras

if __name__ == "__main__":
    cameras = list_available_cameras()
    if cameras:
        print("Kullanılabilir kameralar:")
        for cam in cameras:
            print(f"Kamera {cam}")
    else:
        print("Hiçbir kamera bulunamadı.")
