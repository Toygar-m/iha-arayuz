import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer

class WebcamObjectDetectionApp(QWidget):
    def _init_(self):
        super()._init_()
        self.setWindowTitle("yolo ile görüntü çekme")
        self.resize(800, 600)

        
        self.layout = QVBoxLayout()
        self.label = QLabel("Webcam görüntüsü burada gösterilecek.")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.startButton = QPushButton("Başlat")
        self.startButton.clicked.connect(self.start_detection)
        self.layout.addWidget(self.startButton)

        self.stopButton = QPushButton("Durdur")
        self.stopButton.clicked.connect(self.stop_detection)
        self.layout.addWidget(self.stopButton)

        self.setLayout(self.layout)

        # YOLO dosyaları
        self.cfg_file = "yolo config/yolov4.cfg" 
        self.weights_file = "yolo config/yolov4.weights"  
        self.names_file = "yolo config/coco.names"  

        
        self.net = cv2.dnn.readNetFromDarknet(self.cfg_file, self.weights_file)
        self.classes = []
        with open(self.names_file, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]


        self.cap = cv2.VideoCapture(0)  
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.running = False  

    def start_detection(self):
        if not self.running:
            self.running = True
            self.timer.start(30)  

    def stop_detection(self):
        if self.running:
            self.running = False
            self.timer.stop()
            self.cap.release()
            self.label.clear()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = self.detect_objects(frame)
            self.display_image(frame)

    def detect_objects(self, frame):

        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        layer_names = self.net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        detections = self.net.forward(output_layers)

       
        height, width, _ = frame.shape
        boxes, confidences, class_ids = [], [], []
        for output in detections:
            for detection in output:
                scores = detection[5:]
                class_id = int(scores.argmax())
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x, center_y, w, h = (detection[0:4] * [width, height, width, height]).astype("int")
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, int(w), int(h)])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

       
        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            label = f"{self.classes[class_ids[i]]}: {confidences[i]:.2f}"
            color = (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        return frame

    def display_image(self, image):
       
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_image.shape
        bytes_per_line = channel * width
        q_image = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.label.setPixmap(pixmap.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio))

    def closeEvent(self, event):
      
        self.cap.release()
        self.timer.stop()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebcamObjectDetectionApp()
    window.show()
    sys.exit(app.exec_())