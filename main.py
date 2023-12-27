import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import pygame

# Firebase konfigürasyonu
cred = credentials.Certificate("kapi-c9b42-firebase-adminsdk-cejkv-f2d05ee407.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://kapi-c9b42-default-rtdb.firebaseio.com/",
    'storageBucket': 'kapi-c9b42.appspot.com'
})

bucket = storage.bucket()

# Kamera başlatma
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Arka plan görüntüsü
imgBackground = cv2.imread('Resources/background.png')

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

# Encode dosyasını yükleme
print("Encode Dosyası Yükleniyor...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode Dosyası Yüklendi")

counter = 0

id_printed = False  # Flag to track if the ID has been printed

# ... (Previous code remains unchanged)

# Initialize previous_id and id_not_found flags
previous_id = None
id_not_found = True

# Initialize pygame mixer
pygame.mixer.init()

# Ses dosyasını yükleyin
sound_file_path = "kullanicibulunamadi.mp3"

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 100:100 + 640] = img

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 100 + x1, 162 + y1, x2 - x1, y2 - y1
                bbox_color = (0, 255, 0)  # Green color for recognized face
                cv2.rectangle(imgBackground, (int(bbox[0]), int(bbox[1])), (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])), bbox_color, 2)

                id = studentIds[matchIndex]

                if id != previous_id:  # Check if the ID has changed
                    print(f"Yeni Kullanici ID: {id}")
                    previous_id = id  # Update the previous ID
                    id_not_found = True  # Reset the flag when a new face is detected
                    texttospeakpath=f"Voices/{id}.mp3"
                    pygame.mixer.music.load(texttospeakpath)
                    pygame.mixer.music.play()
                      
        
            else:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - x1
                bbox_color = (0, 0, 255)  # Red color for unrecognized face
                cv2.rectangle(imgBackground, (int(bbox[0]), int(bbox[1])), (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])), bbox_color, 2)
            

                if not id_printed and id_not_found:
                    print("Kullanici Bulunamadi")
                    id_printed = True
                    pygame.mixer.music.load(sound_file_path)
                    pygame.mixer.music.play()
                    previous_id=-1
                    id_not_found = False  # Set the flag to False to indicate that the message has been printed

                # Reset the flag when a new face is detected
                id_printed = False



    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
