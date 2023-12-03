import cv2
import numpy as np
import requests
#from io import BytesIO

#ESP32 URL
# URL = 'http://192.168.0.101'
# AWB = True
# res = requests.get(URL, stream = (True))

#cap = cv2.VideoCapture(URL + ":81/stream")

# while True:
#    if cap.isOpened():
#        Success, frame = cap.read()

#        cv2.imshow("frame", frame)

#    if cv2.waitKey(1):
#        break

#cv2.waitKey(1)
#cv2.destroyAllWindows()
#cap.release() 

# for chunk in res.iter_content(chunk_size = 120000):
#     if len(chunk) > 100:
#         try: img_data = BytesIO

# Adres IP kamery ESP
# esp_ip = "192.168.0.101"  # Zmień na adres IP swojej kamery ESP

# Adres URL strumienia MJPEG z kamery ESP
# stream_url = f"http://{esp_ip}/mjpeg/1"
stream_url = f"http://192.168.0.101:81/stream"

# Utwórz obiekt VideoCapture do odbierania strumienia
cap = cv2.VideoCapture(stream_url)

while True:
    # Odczytaj klatkę z strumienia
    ret, frame = cap.read()

    if not ret:
        print("Błąd podczas odczytu klatki")
        break

    # Wyświetl klatkę
    cv2.imshow("Kamera ESP", frame)

    # Przerwij pętlę po naciśnięciu klawisza 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Zwolnij zasoby
cap.release()
cv2.destroyAllWindows()
