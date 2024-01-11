import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from subprocess import Popen

class AnaPencere(QWidget):
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

        # Ana pencereye düzeni ekle
        self.setLayout(vbox)

        # Pencere boyutlarını ayarla
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Ana Pencere')
        self.show()


    def proje_ac(self):
        # main.py dosyasını çalıştır
        Popen(['python', 'start_ui.py'])



    def pencere2_ac(self):
        # Pencere 2'nin olduğu sınıfı oluştur ve göster
        Popen(['python', 'register.py'])
        self.close()

class Pencere2(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Pencere 2')
        self.setGeometry(100, 100, 800, 600)  # Pencere boyutlarını dilediğiniz gibi ayarlayabilirsiniz

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ana_pencere = AnaPencere()
    sys.exit(app.exec_())
