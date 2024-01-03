import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap

class PhotoViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)

        open_button = QPushButton('Fotoğraf Aç', self)
        open_button.clicked.connect(self.openImage)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(open_button)

        self.setLayout(layout)

    def openImage(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Fotoğraf Seç', '', 'Resim Dosyaları (*.png *.jpg *.jpeg *.bmp)')

        if file_path:
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = PhotoViewer()
    viewer.show()
    sys.exit(app.exec_())
