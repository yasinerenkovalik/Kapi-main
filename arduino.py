import serial
import time

arduino_port = "/dev/cu.usbserial-10"  # Arduino'nun bağlı olduğu portu belirtin (COMX'i Arduino'nun bağlı olduğu port ile değiştirin)
baud_rate = 9600  # Arduino kodundaki baud oranı ile aynı olmalı

ser = serial.Serial(arduino_port, baud_rate, timeout=1)

time.sleep(2)  # Arduino'nun başlaması için biraz bekle

while True:
    user_input = input("LED'i açmak için '1', kapatmak için '0' girin: ")
    ser.write(user_input.encode())  # Kullanıcının girdiğini Arduino'ya gönder