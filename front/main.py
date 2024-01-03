import os
import pickle
import numpy as np
import cv2
import face_recognition
import pygame

def Proje():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    folderModePath = '../Resources/Modes'
    modePathList = os.listdir(folderModePath)

    imgModeList = []

    for path in modePathList:
        img = cv2.imread(os.path.join(folderModePath, path))
        if img is None:
            print(f"Hata: {path} yüklenemedi.")
        else:
            imgModeList.append(img)

    print("Encode Dosyası Yükleniyor...")
    file = open('../EncodeFile.p', 'rb')
    encodeListKnownWithIds = pickle.load(file)
    file.close()
    encodeListKnown, studentIds = encodeListKnownWithIds
    print("Encode Dosyası Yüklendi")

    id_printed = False
    previous_id = None
    id_not_found = True

    pygame.mixer.init()
    sound_file_path = "../kullanicibulunamadi.mp3"

    while True:
        success, img = cap.read()

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        if faceCurFrame:
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

                    # Yüzü yeşil bir kare içine al
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    id = studentIds[matchIndex]

                    if id != previous_id:
                        print(f"Yeni Kullanici ID: {id}")
                        previous_id = id
                        id_not_found = True
                        texttospeakpath = f"../Voices/{id}.mp3"
                        pygame.mixer.music.load(texttospeakpath)
                        pygame.mixer.music.play()

                else:
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

                    # Yüzü yeşil bir kare içine al
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - x1

                    if not id_printed and id_not_found:
                        print("Kullanici Bulunamadi")
                        id_printed = True
                        pygame.mixer.music.load(sound_file_path)
                        pygame.mixer.music.play()
                        previous_id = -1
                        id_not_found = False

                    id_printed = False

        cv2.imshow("Face Attendance", img)
        cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

Proje()
