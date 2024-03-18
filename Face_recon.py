import cv2

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)
ancho = int(cap.get(5))
alto = int(cap.get(5))

print(ancho,alto)

while True:
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    #x, y, w, h son los vertices del cuadrado
    for(x, y, w, h) in faces:
        #                                       color     Espesor
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2) #Se dibuja sobre el rostro al detectarlo
    
    cv2.imshow('img', img)
    k = cv2.waitKey(30) #Detecta la letra escape para salir del programa
    if k == 27: #27 es la letra ASCII para el esc 
        cv2.destroyAllWindows()
        break
    
cap.release()
        