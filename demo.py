from imageai.Detection import FaceDetection
from cv2 import cv2
import os

# Mod görüntülerini içeren liste
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []

# Görüntülerin yüklenmesi
for path in modePathList:
    img = cv2.imread(os.path.join(folderModePath, path))
    if img is None:
        print(f"Hata: {path} yüklenemedi.")
    else:
        imgModeList.append(img)

# Resimden yüz algılama
detector = FaceDetection()
detector.setModelTypeAsHaarCascade()
detector.setModelPath("haarcascade_frontalface_default.xml")

input_path = "path_to_image.jpg"
output_path = "path_to_output_image.jpg"

detector.detectFacesFromImage(input_image=input_path, output_image_path=output_path)

print(f"{len(detector.faces)} yüz bulundu")

for face in detector.faces:
    print(f"Yüz algılandı: X: {face['topleft']['x']}, Y: {face['topleft']['y']}, Genişlik: {face['width']}, Yükseklik: {face['height']}")