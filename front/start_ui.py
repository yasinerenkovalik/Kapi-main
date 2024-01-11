import os
import pickle
import numpy as np
import cv2
import face_recognition
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import serial
import time

class FaceRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.cap = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_frame)

        # Arduino bağlantısı ve önceki durum kontrolü için değişkenler
        self.ser = None
        self.previous_id = None
        self.id_not_found = True

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Face Recognition App')

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)

        self.start_button = QPushButton('Başlat', self)
        self.start_button.clicked.connect(self.start_recognition)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Durdur', self)
        self.stop_button.clicked.connect(self.stop_recognition)
        self.layout.addWidget(self.stop_button)



        self.central_widget.setLayout(self.layout)

        self.sound_file_path = "../kullanicibulunamadi.mp3"
        self.id_printed = False
        self.previous_id = None
        self.id_not_found = True

    def start_recognition(self):
        if not self.timer.isActive():
            self.cap = cv2.VideoCapture(0)
            self.cap.set(3, 640)
            self.cap.set(4, 480)
            self.timer.start(30)
            self.load_encodings()

            # Arduino'ya bağlan
            #self.connect_to_arduino()

    def stop_recognition(self):
        if self.timer.isActive():
            self.cap.release()
            self.timer.stop()
            # Arduino bağlantısını kapat
           # self.disconnect_from_arduino()

    def load_encodings(self):
        print("Encode Dosyası Yükleniyor...")
        file = open('../EncodeFile.txt', 'rb')
        encodeListKnownWithIds = pickle.load(file)
        file.close()
        self.encodeListKnown, self.studentIds = encodeListKnownWithIds
        print("Encode Dosyası Yüklendi")



    def Proje(self):
        success, img = self.cap.read()

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_RGB2BGR)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        if faceCurFrame:
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)

                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    id = self.studentIds[matchIndex]

                    if id != self.previous_id:
                        print(f"Yeni Kullanici ID: {id}")
                        self.previous_id = id
                        self.id_not_found = True

                        # Arduino'ya 1 gönder
                        #self.send_to_arduino('1')

                else:
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - x1

                    if not self.id_printed and self.id_not_found:
                        print("Kullanici Bulunamadi")
                        self.id_not_found = True
                        # Arduino'ya 0 gönder
                        self.send_to_arduino('0')
                        self.previous_id = -1
                        self.id_not_found = False
                    self.id_printed = False

        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img.rgbSwapped())
        self.image_label.setPixmap(pixmap)

    def send_to_arduino(self, message):
        if self.ser is not None:
            self.ser.write(message.encode())

    def show_frame(self):
        self.Proje()

if __name__ == '__main__':
    app = QApplication([])
    mainWin = FaceRecognitionApp()
    mainWin.show()
    app.exec_()
