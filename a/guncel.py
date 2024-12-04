from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import numpy as np
import time
from multiprocessing import Process, Queue, freeze_support


def yolo_process(frame_queue, processed_queue, config_path, weights_path, names_path):
    """YOLO modelini çalıştıran süreç."""
    net = cv2.dnn.readNet(weights_path, config_path)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    with open(names_path, "r") as f:
        classes = [line.strip() for line in f.readlines()]

    while True:
        frame = frame_queue.get()
        if frame is None:  # Ana süreçten None alındığında çık
            break

        height, width, channels = frame.shape
        net_input = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(net_input)
        outs = net.forward([net.getLayerNames()[i - 1] for i in net.getUnconnectedOutLayers()])

        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.2:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        for i in range(len(boxes)):
            if i in cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3):
                x, y, w, h = boxes[i]
                color = (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.rectangle(frame, (x, y), (x + w, y + 30), color, -1)
                cv2.putText(frame, str(classes[class_ids[i]]) + " " + str(round(confidences[i], 2)), (x, y + 30),
                            cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

        processed_queue.put(frame)


class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open video stream or file")
            exit()

        self.starting_time = time.time()
        self.frame_id = 0

        # Multiprocessing Kuyrukları
        self.frame_queue = Queue(maxsize=1)  # Çerçeve gönderim kuyruğu
        self.processed_queue = Queue(maxsize=1)  # İşlenmiş çerçeve kuyruğu

        # YOLO Süreci
        self.yolo_process = Process(target=yolo_process,
                                    args=(self.frame_queue, self.processed_queue,
                                          "./yolo/yolov4.cfg", "./yolo/yolov4.weights", "./yolo/coco.names"))
        self.yolo_process.start()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setStyleSheet("background-color: #373737;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_38 = QtWidgets.QLabel(self.centralwidget)
        self.label_38.setGeometry(QtCore.QRect(26, 82, 881, 911))
        self.label_38.setStyleSheet("background-color: black;")
        self.label_38.setText("")
        self.label_38.setObjectName("label_38")
        self.label_38.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Timer Ayarları
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.guncelle)
        self.timer.start(30)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def guncelle(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        self.frame_id += 1
        elapsed_time = time.time() - self.starting_time
        fps = self.frame_id / elapsed_time
        cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

        # Ham çerçeveyi YOLO sürecine gönder
        if not self.frame_queue.full():
            self.frame_queue.put(frame)

        # İşlenmiş çerçeveyi kuyruğundan al ve göster
        if not self.processed_queue.empty():
            processed_frame = self.processed_queue.get()
            rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            self.label_38.setPixmap(
                QtGui.QPixmap.fromImage(QtGui.QImage(rgb_frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888))
            )

    def closeEvent(self, event):
        """Pencere kapatıldığında süreçleri temizle."""
        self.cap.release()
        self.frame_queue.put(None)  # YOLO sürecine sonlanma sinyali gönder
        self.yolo_process.join()  # Sürecin bitmesini bekle


if __name__ == "__main__":
    freeze_support()
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
