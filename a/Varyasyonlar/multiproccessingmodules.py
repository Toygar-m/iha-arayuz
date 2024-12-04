from PyQt5 import QtCore, QtGui, QtWidgets
import cv2, time, sys, os, signal
from ultralytics import YOLO
from multiprocessing import Process, Queue, freeze_support


def yolo_process(queue, output_queue, fps_queue):
    model = YOLO('yolov8n.pt')
    while True:
        frame = queue.get()
        if frame is None: break
        start_time = time.time()
        processed_frame = model(frame)[0].plot()
        end_time = time.time()
        output_queue.put(processed_frame)
        fps_queue.put(1 / (end_time - start_time))


class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open video stream or file")
            exit()

        self.starting_time = time.time()
        self.frame_id = 0

        self.frame_queue = Queue(maxsize=1) 
        self.processed_queue = Queue(maxsize=1)  
        self.fps_queue = Queue(maxsize=1)

        self.yolo_process = Process(target=yolo_process, args=(self.frame_queue, self.processed_queue, self.fps_queue))
        self.yolo_process.start()
        self.current_fps = 0
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setStyleSheet("background-color: #373737;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 10, 51, 51))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Folders/IMG/topkapi-bg.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(90, 20, 351, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: white;")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1310, 20, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: white;")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(1270, 20, 31, 31))
        self.label_4.setStyleSheet("color: white;")
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("Folders/IMG/date.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(0, 60, 1920, 15))
        self.label_5.setStyleSheet("border: 2px solid #424242 ; border-top: none; border-left: none; border-right: none;")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(1490, 20, 31, 31))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("Folders/IMG/clock-bg.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(1530, 20, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: white;")
        self.label_7.setObjectName("label_7")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(999, 79, 491, 221))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_16 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_16.setStyleSheet("color: red;")
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 7, 0, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_17.setStyleSheet("color: white;")
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 0, 1, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_21.setStyleSheet("color: white;")
        self.label_21.setObjectName("label_21")
        self.gridLayout.addWidget(self.label_21, 4, 1, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_18.setStyleSheet("color: white;")
        self.label_18.setObjectName("label_18")
        self.gridLayout.addWidget(self.label_18, 1, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_13.setStyleSheet("color: red;")
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 4, 0, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_22.setStyleSheet("color: white;")
        self.label_22.setObjectName("label_22")
        self.gridLayout.addWidget(self.label_22, 5, 1, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_24.setStyleSheet("color: white;")
        self.label_24.setObjectName("label_24")
        self.gridLayout.addWidget(self.label_24, 7, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_12.setStyleSheet("color: red;")
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 3, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_14.setStyleSheet("color: red;")
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 5, 0, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_20.setStyleSheet("color: white;")
        self.label_20.setObjectName("label_20")
        self.gridLayout.addWidget(self.label_20, 3, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_15.setStyleSheet("color: red;")
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 6, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_11.setStyleSheet("color: red;")
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 2, 0, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_23.setStyleSheet("color: white;")
        self.label_23.setObjectName("label_23")
        self.gridLayout.addWidget(self.label_23, 6, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_10.setStyleSheet("color: red;")
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_9.setStyleSheet("color: red;")
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_19.setStyleSheet("color: white;")
        self.label_19.setObjectName("label_19")
        self.gridLayout.addWidget(self.label_19, 2, 1, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(1541, 81, 351, 211))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_3.setStyleSheet("color: white; height: 35; margin-right: 10px")
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_2.addWidget(self.pushButton_3, 2, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton.setStyleSheet("color: white; height: 35; margin-right: 10px")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_2.setStyleSheet("color: white; height: 35; margin-right: 10px")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 1, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_4.setStyleSheet("color: white; height: 35; margin-left: 10px")
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_2.addWidget(self.pushButton_4, 0, 1, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_5.setStyleSheet("color: white; height: 35; margin-left: 10px")
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_2.addWidget(self.pushButton_5, 1, 1, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_6.setStyleSheet("color: white; height: 35px; margin-left: 10px; ")
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout_2.addWidget(self.pushButton_6, 2, 1, 1, 1)
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(1000, 320, 491, 151))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_30 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_30.setStyleSheet("color: white;")
        self.label_30.setObjectName("label_30")
        self.gridLayout_3.addWidget(self.label_30, 2, 1, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_25.setStyleSheet("color: red;")
        self.label_25.setObjectName("label_25")
        self.gridLayout_3.addWidget(self.label_25, 1, 0, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_26.setStyleSheet("color: red;")
        self.label_26.setObjectName("label_26")
        self.gridLayout_3.addWidget(self.label_26, 0, 0, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_29.setStyleSheet("color: white;")
        self.label_29.setObjectName("label_29")
        self.gridLayout_3.addWidget(self.label_29, 1, 1, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_28.setStyleSheet("color: white;")
        self.label_28.setObjectName("label_28")
        self.gridLayout_3.addWidget(self.label_28, 0, 1, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_27.setStyleSheet("color: red;")
        self.label_27.setObjectName("label_27")
        self.gridLayout_3.addWidget(self.label_27, 2, 0, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.pushButton_7.setStyleSheet("color: white; height: 30; margin-right: 10px")
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_3.addWidget(self.pushButton_7, 3, 0, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.pushButton_8.setStyleSheet("color: white; height: 30; margin-left: 10px")
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout_3.addWidget(self.pushButton_8, 3, 1, 1, 1)
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(1540, 320, 351, 151))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.pushButton_9 = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.pushButton_9.setStyleSheet("color: white; height: 30; margin-right: 10px")
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout_4.addWidget(self.pushButton_9, 2, 0, 1, 1)
        self.label_32 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_32.setStyleSheet("color: red;")
        self.label_32.setObjectName("label_32")
        self.gridLayout_4.addWidget(self.label_32, 1, 0, 1, 1)
        self.pushButton_10 = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.pushButton_10.setStyleSheet("color: white; height: 30; margin-left: 10px")
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout_4.addWidget(self.pushButton_10, 2, 1, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_31.setStyleSheet("color: red;")
        self.label_31.setObjectName("label_31")
        self.gridLayout_4.addWidget(self.label_31, 0, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.gridLayoutWidget_4)
        self.comboBox.setStyleSheet("color: white; margin-left: 10px; height: 20;")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout_4.addWidget(self.comboBox, 0, 1, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.gridLayoutWidget_4)
        self.comboBox_2.setStyleSheet("color: white; margin-left: 10px; height: 20;")
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.gridLayout_4.addWidget(self.comboBox_2, 1, 1, 1, 1)
        self.label_35 = QtWidgets.QLabel(self.centralwidget)
        self.label_35.setGeometry(QtCore.QRect(1700, 20, 31, 31))
        self.label_35.setText("")
        self.label_35.setPixmap(QtGui.QPixmap("Folders/IMG/ucak.png"))
        self.label_35.setScaledContents(True)
        self.label_35.setObjectName("label_35")
        self.label_36 = QtWidgets.QLabel(self.centralwidget)
        self.label_36.setGeometry(QtCore.QRect(1740, 20, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_36.setFont(font)
        self.label_36.setStyleSheet("color: white;")
        self.label_36.setObjectName("label_36")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(1510, 80, 20, 391))
        self.label_8.setStyleSheet("border: 2px solid #424242 ; border-top: none; border-right: none; border-bottom: none;")
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.label_37 = QtWidgets.QLabel(self.centralwidget)
        self.label_37.setGeometry(QtCore.QRect(1000, 300, 1980, 10))
        self.label_37.setStyleSheet("border: 2px solid #424242 ; border-top: none; border-left: none; border-right: none;")
        self.label_37.setText("")
        self.label_37.setObjectName("label_37")
        self.label_38 = QtWidgets.QLabel(self.centralwidget)
        self.label_38.setGeometry(QtCore.QRect(26, 82, 881, 911))
        self.label_38.setStyleSheet("background-color: black;")
        self.label_38.setText("")
        self.label_38.setObjectName("label_38")
        
        self.label_8.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.gridLayoutWidget.raise_()
        self.gridLayoutWidget_2.raise_()
        self.gridLayoutWidget_3.raise_()
        self.gridLayoutWidget_4.raise_()
        self.label_35.raise_()
        self.label_36.raise_()
        self.label_37.raise_()
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

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.guncelle)
        self.timer.start(30)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "TOPKAPI İNSANSIZ HAVA ARACI"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">27.11.2024</p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">21:19:43</p></body></html>"))
        self.label_16.setText(_translate("MainWindow", "MOD DURUMU"))
        self.label_17.setText(_translate("MainWindow", "123"))
        self.label_21.setText(_translate("MainWindow", "554"))
        self.label_18.setText(_translate("MainWindow", "3424"))
        self.label_13.setText(_translate("MainWindow", "HAVA HIZI"))
        self.label_22.setText(_translate("MainWindow", "342"))
        self.label_24.setText(_translate("MainWindow", "3423"))
        self.label_12.setText(_translate("MainWindow", "ARAÇ HIZI"))
        self.label_14.setText(_translate("MainWindow", "YER HIZI"))
        self.label_20.setText(_translate("MainWindow", "4324"))
        self.label_15.setText(_translate("MainWindow", "ARAÇ YÜKSEKLİĞİ"))
        self.label_11.setText(_translate("MainWindow", "YAW ACISI"))
        self.label_23.setText(_translate("MainWindow", "432"))
        self.label_10.setText(_translate("MainWindow", "PİTCH AÇISI"))
        self.label_9.setText(_translate("MainWindow", "ROLL AÇISI"))
        self.label_19.setText(_translate("MainWindow", "342"))
        self.pushButton_3.setText(_translate("MainWindow", "RTL"))
        self.pushButton.setText(_translate("MainWindow", "FBWA"))
        self.pushButton_2.setText(_translate("MainWindow", "MANUAL"))
        self.pushButton_4.setText(_translate("MainWindow", "FBWB"))
        self.pushButton_5.setText(_translate("MainWindow", "AUTOTUNE"))
        self.pushButton_6.setText(_translate("MainWindow", "AUTO"))
        self.label_30.setText(_translate("MainWindow", "TextLabel"))
        self.label_25.setText(_translate("MainWindow", "KİTLENME SÜRESİ"))
        self.label_26.setText(_translate("MainWindow", "KİTLENME DURUMU"))
        self.label_29.setText(_translate("MainWindow", "TextLabel"))
        self.label_28.setText(_translate("MainWindow", "TextLabel"))
        self.label_27.setText(_translate("MainWindow", "KİTLENME SAYISI"))
        self.pushButton_7.setText(_translate("MainWindow", "ARMED"))
        self.pushButton_8.setText(_translate("MainWindow", "DİSARMED"))
        self.pushButton_9.setText(_translate("MainWindow", "BAĞLAN"))
        self.label_32.setText(_translate("MainWindow", "BAUD"))
        self.pushButton_10.setText(_translate("MainWindow", "BAĞLANTIYI KES"))
        self.label_31.setText(_translate("MainWindow", "PORT"))
        self.comboBox.setItemText(0, _translate("MainWindow", "13123,"))
        self.comboBox.setItemText(1, _translate("MainWindow", "dwdw"))
        self.comboBox.setItemText(2, _translate("MainWindow", "wdwdwd"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "13123,"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "dwdw"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "wdwdwd"))
        self.label_36.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">00:00:00</p></body></html>"))
        
    def guncelle(self):
        ret, frame = self.cap.read()
        if not ret: return
        if not self.frame_queue.full(): self.frame_queue.put(frame)
        if not self.processed_queue.empty():
            processed_frame = self.processed_queue.get()

            if not self.fps_queue.empty(): self.current_fps = self.fps_queue.get()

            cv2.putText(processed_frame, f"FPS: {self.current_fps:.2f}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA, )

            rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            self.label_38.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(rgb_frame.data, w, h, ch * w, QtGui.QImage.Format_RGB888)))    

if __name__ == "__main__":
    freeze_support()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())