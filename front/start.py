import sys
import pickle
import cv2
import face_recognition
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from subprocess import Popen

class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # İki buton oluştur
        buton1 = QPushButton('Projemi Aç', self)
        buton2 = QPushButton('Pencere 2', self)

        # Butonlara tıklandığında çağrılacak işlevleri belirle
        buton1.clicked.connect(self.proje_ac)
        buton2.clicked.connect(self.pencere2_ac)

        # Dikey bir düzen oluştur
        vbox = QVBoxLayout()
        vbox.addWidget(buton1)
        vbox.addWidget(buton2)

        # Merkezi bir widget oluştur ve düzeni ekleyin
        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

        # Pencere boyutlarını ayarla
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Ana Pencere')

    def proje_ac(self):
        # main.py dosyasını çalıştır
        self.hide()  # Ana pencereyi gizle
        self.proje_pencere = FaceRecognitionApp(self)
        self.proje_pencere.show()

    def pencere2_ac(self):
        # Pencere 2'nin olduğu sınıfı oluştur ve göster
        self.hide()  # Ana pencereyi gizle
        self.pencere2 = Pencere2(self)
        self.pencere2.show()

class FaceRecognitionApp(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.cap = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_frame)

        self.initUI()

        self.sound_file_path = "../kullanicibulunamadi.mp3"
        self.id_printed = False
        self.previous_id = None
        self.id_not_found = True

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Face Recognition App')

        self.layout = QVBoxLayout()

        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)

        self.start_button = QPushButton('Başlat', self)
        self.start_button.clicked.connect(self.start_recognition)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Durdur', self)
        self.stop_button.clicked.connect(self.stop_recognition)
        self.layout.addWidget(self.stop_button)

        self.setLayout(self.layout)

    def start_recognition(self):
        if not self.timer.isActive():
            self.cap = cv2.VideoCapture(0)
            self.cap.set(3, 640)
            self.cap.set(4, 480)
            self.timer.start(30)
            self.load_encodings()

    def stop_recognition(self):
        if self.timer.isActive():
            self.cap.release()
            self.timer.stop()

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
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

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

                    # Yüzü yeşil bir kare içine al
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    id = self.studentIds[matchIndex]

                    if id != self.previous_id:
                        print(f"Yeni Kullanici ID: {id}")
                        self.previous_id = id
                        self.id_not_found = True

                else:
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

                    # Yüzü yeşil bir kare içine al
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - x1

                    if not self.id_printed and self.id_not_found:
                        print("Kullanici Bulunamadi")
                        self.id_printed = True

                        self.previous_id = -1
                        self.id_not_found = False

                    self.id_printed = False

        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.image_label.setPixmap(pixmap)

    def show_frame(self):
        self.Proje()

class Pencere2(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Pencere 2')
        self.setGeometry(100, 100, 800, 600)  # Pencere boyutlarını dilediğiniz gibi ayarlayabilirsiniz

    def closeEvent(self, event):
        self.parent().show()  # Pencere kapatıldığında ana pencereyi göster

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ana_pencere = AnaPencere()
    ana_pencere.show()
    sys.exit(app.exec_())
