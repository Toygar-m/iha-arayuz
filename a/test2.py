import sys
import cv2
import math
import mediapipe as mp
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QFont

carpan = 0.0015 

mp_poz = mp.solutions.pose
mp_cizim = mp.solutions.drawing_utils
poz = mp_poz.Pose()

class KameraUygulamasi(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.cap = cv2.VideoCapture(0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.guncelle)

        self.timer.start(30)

    def initUI(self):
        self.label_38 = QLabel()
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox.addLayout(vbox)
        hbox.addWidget(self.label_38)

        self.setLayout(hbox)
        self.setWindowTitle('Poz Tespiti ve Boy Tahmini')
        self.setGeometry(100, 100, 800, 600)
        self.showFullScreen()

    def guncelle(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        rgbGoruntu = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgbGoruntu.shape
        bytes_per_line = ch * w
        self.label_38.setPixmap(QPixmap.fromImage(QImage(rgbGoruntu.data, w, h, bytes_per_line, QImage.Format_RGB888)))

    def closeEvent(self, event):
        self.cap.release()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    kamera_uygulamasi = KameraUygulamasi()
    kamera_uygulamasi.show()
    sys.exit(app.exec_())
