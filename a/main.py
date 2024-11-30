import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGridLayout, QWidget, QLineEdit, QGroupBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, QDateTime


class UAVControlPanel(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Göktürk İnsansız Hava Aracı Kontrol Paneli")
        self.setGeometry(100, 100, 1024, 768)

        # Ana widget ve layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QGridLayout(self.central_widget)

        # Kamera Görüntüsü Alanı
        self.camera_label = QLabel("KAMERA")
        self.camera_label.setFixedSize(400, 300)
        self.camera_label.setStyleSheet("border: 2px solid black;")
        self.camera_label.setPixmap(QPixmap("placeholder.jpg").scaled(400, 300))  # Placeholder image

        # Veri Göstergeleri
        self.data_layout = QVBoxLayout()
        self.roll_label = QLabel("ROLL AÇISI: 0.000")
        self.pitch_label = QLabel("PITCH AÇISI: 0.000")
        self.yaw_label = QLabel("YAW AÇISI: 0.000")
        self.speed_label = QLabel("ARAÇ HIZI: 0.000")
        self.altitude_label = QLabel("ARAÇ YÜKSEKLİĞİ: 0.000")
        self.data_labels = [
            self.roll_label, self.pitch_label, self.yaw_label,
            self.speed_label, self.altitude_label
        ]

        for label in self.data_labels:
            label.setStyleSheet("font-size: 14px;")
            self.data_layout.addWidget(label)

        # Butonlar
        self.button_layout = QVBoxLayout()
        self.fbwa_button = QPushButton("FBWA")
        self.fbwb_button = QPushButton("FBWB")
        self.manual_button = QPushButton("MANUAL")
        self.autotune_button = QPushButton("AUTOTUNE")
        self.rtl_button = QPushButton("RTL")
        self.auto_button = QPushButton("AUTO")
        self.buttons = [
            self.fbwa_button, self.fbwb_button, self.manual_button,
            self.autotune_button, self.rtl_button, self.auto_button
        ]

        for button in self.buttons:
            button.setFixedSize(120, 50)
            self.button_layout.addWidget(button)

        # Durum Göstergesi
        self.arm_disarm_layout = QHBoxLayout()
        self.armed_button = QPushButton("ARMED")
        self.disarmed_button = QPushButton("DISARMED")
        self.armed_button.setStyleSheet("background-color: green; color: white;")
        self.disarmed_button.setStyleSheet("background-color: red; color: white;")
        self.armed_button.setFixedSize(120, 50)
        self.disarmed_button.setFixedSize(120, 50)

        self.arm_disarm_layout.addWidget(self.armed_button)
        self.arm_disarm_layout.addWidget(self.disarmed_button)

        # Üst Bilgi: Tarih ve Saat
        self.top_layout = QHBoxLayout()
        self.date_label = QLabel(QDateTime.currentDateTime().toString("dd/MM/yyyy"))
        self.time_label = QLabel(QDateTime.currentDateTime().toString("HH:mm:ss"))
        self.top_layout.addWidget(self.date_label)
        self.top_layout.addWidget(self.time_label)

        # Saat Güncelleyici
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        # Layoutları Birleştirme
        self.main_layout.addLayout(self.top_layout, 0, 0, 1, 2)
        self.main_layout.addWidget(self.camera_label, 1, 0)
        self.main_layout.addLayout(self.data_layout, 1, 1)
        self.main_layout.addLayout(self.button_layout, 2, 1)
        self.main_layout.addLayout(self.arm_disarm_layout, 3, 1)

    def update_time(self):
        """Saat ve tarih güncelleme."""
        self.date_label.setText(QDateTime.currentDateTime().toString("dd/MM/yyyy"))
        self.time_label.setText(QDateTime.currentDateTime().toString("HH:mm:ss"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UAVControlPanel()
    window.show()
    sys.exit(app.exec_())
