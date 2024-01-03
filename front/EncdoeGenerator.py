import cv2
import face_recognition
import pickle
import os

folderPath = '../Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []
def EncodeStart():
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

EncodeStart()