import sys
import pickle
import face_recognition
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QFileDialog, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
import firebase_admin
from firebase_admin import credentials, db
import random
import cv2
import os

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.key = self.generate_unique_key()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ad, Soyad ve Fotoğraf')
        self.setGeometry(100, 100, 800, 600) 

        self.name_label = QLabel('Ad:')
        self.name_edit = QLineEdit(self)

        self.surname_label = QLabel('Soyad:')
        self.surname_edit = QLineEdit(self)

        self.photo_label = QLabel('Fotoğraf:')
        self.photo_path = None

        self.browse_button = QPushButton('Gözat', self)
        self.browse_button.clicked.connect(self.browse_image)

        self.show_button = QPushButton('Ekle', self)
        self.show_button.clicked.connect(self.show_info)

        # Layout
        layout = QVBoxLayout()

        # Ad ve Soyad etiketleri ve inputları için horizontal layout
        name_layout = QHBoxLayout()
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        surname_layout = QHBoxLayout()
        surname_layout.addWidget(self.surname_label)
        surname_layout.addWidget(self.surname_edit)
        layout.addLayout(surname_layout)

        # Fotoğraf etiketi, gösterme alanı ve butonları için horizontal layout
        photo_layout = QHBoxLayout()
        photo_layout.addWidget(self.photo_label)
        photo_layout.addWidget(self.browse_button)
        photo_layout.addWidget(self.show_button)
        layout.addLayout(photo_layout)

        self.setLayout(layout)

    def browse_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
     
        file_name, _ = QFileDialog.getOpenFileName(self, "Fotoğraf Seç", "", "Resim Dosyaları (*.png;*.jpg;*.bmp;*.jpeg)", options=options)

        if file_name:
            # Yüz tespiti yap
            face_image = self.detect_face(file_name)
            
            # Eğer yüz bulunduysa, başka bir dosyaya kaydet
            if face_image is not None:
                face_file_name = f"../Images/{self.key}.png"

                cv2.imwrite(face_file_name, cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB))# OpenCV ile BGR formatında kaydedildiği için dönüştürme yapıyoruz

                self.show_detected_face(face_file_name)
                print("dosya kaydedildi")

            self.EncodeStart()
    def EncodeStart(self):
        folderPath = '../Images'
        pathList = os.listdir(folderPath)
        print(pathList)
        imgList = []
        studentIds = []
        for path in pathList:
            img_path = os.path.join(folderPath, path)

            # Resim dosyasının var olup olmadığını kontrol et
            if not os.path.exists(img_path):
                print(f"Hata: {img_path} dosyası bulunamadı.")
                continue

            img = cv2.imread(img_path)
            if img is None:
                print(f"Hata: {img_path} dosyası bir resim dosyası değil veya okunamıyor.")
                continue

            imgList.append(img)
            studentIds.append(os.path.splitext(path)[0])

            fileName = f'{folderPath}/{path}'
            # print(path)
            # print(os.path.splitext(path)[0])
        print(studentIds)


        def findEncodings(imagesList):
            encodeList = []
            for img in imagesList:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)

            return encodeList

        print("Encoding Started ...")
        encodeListKnown = findEncodings(imgList)
        encodeListKnownWithIds = [encodeListKnown, studentIds]
        print("Encoding Complete")

        # EncodeFile.txt dosyasını kontrol et
        if os.path.exists("../EncodeFile.txt"):
            os.remove("../EncodeFile.txt")
            print("Existing EncodeFile.txt removed.")

        # Yeni dosyayı oluştur ve verileri kaydet
        file = open("../EncodeFile.txt", 'wb')
        pickle.dump(encodeListKnownWithIds, file)
        file.close()
        print("File Saved")
    def detect_face(self, image_path):
        # OpenCV ile yüz tespiti yap
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # Eğer yüz bulunduysa, ilk yüzü al
        if len(faces) > 0:
            x, y, w, h = faces[0]
            face_image = img[y:y+h, x:x+w]
            return face_image
        else:
            return None

    def show_detected_face(self, face_file_name):
        # Load the image using OpenCV
        img = cv2.imread(face_file_name)

        # Convert BGR to RGB color order
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Create a QPixmap from the converted image
        pixmap = QPixmap.fromImage(
        QImage(img_rgb.data, img_rgb.shape[1], img_rgb.shape[0], img_rgb.shape[1] * 3, QImage.Format_RGB888))

        # Set the pixmap to the QLabel
        self.photo_label.setPixmap(pixmap.scaledToWidth(150))

    def show_info(self):
        name = self.name_edit.text()
        surname = self.surname_edit.text()

        if name and surname:
            info_str = f"Ad: {name}\nSoyad: {surname}"
            self.photo_label.setText(info_str)
            if self.photo_path:
                pixmap = QPixmap(self.photo_path)
                self.photo_label.setPixmap(pixmap.scaledToWidth(150))

            # Firebase'e veri ekle
            
            data = {
                self.key: {
                    "name": name,
                    "surname": surname,
                }
            }
            ref = db.reference("PromotedPerson")
            ref.update(data)




    def generate_unique_key(self):
        # 6 haneli rastgele sayı oluştur
        return str(random.randint(100000, 999999))



if __name__ == '__main__':
    cred = credentials.Certificate("../kapi-c9b42-firebase-adminsdk-cejkv-f2d05ee407.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://kapi-c9b42-default-rtdb.firebaseio.com/"
    })

    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
