import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap


class KameraUygulamasi(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Kamera açılamadı")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.guncelle)
        self.timer.start(30)

    def guncelle(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Kare yakalanamadı")
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        step = channel * width
        q_image = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.goruntu_label.setPixmap(pixmap)

    def initUI(self):
        self.goruntu_label = QLabel("Kamera yükleniyor")
        self.goruntu_label.setAlignment(Qt.AlignCenter)

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox.addWidget(self.goruntu_label)
        hbox.addLayout(vbox)

        self.setLayout(hbox)
        self.setWindowTitle('Poz Tespiti ve Boy Tahmini')
        self.setGeometry(100, 100, 800, 600)
        self.show()

    def closeEvent(self, event):
        self.cap.release()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        kamera_uygulamasi = KameraUygulamasi()
        kamera_uygulamasi.show()
        sys.exit(app.exec_())
    except RuntimeError as e:
        print(str(e))
        sys.exit(1)

