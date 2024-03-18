import cv2
import imutils

cap = cv2.VideoCapture(0,cv2.CAP_MSMF)
bg = None
color_contorno = (0,255,0)
color_ymin = (0,130,255)
color_zona1 = (0,255,255)
color_zona2 = (0,0,255)

while True:
    
    ret, frame = cap.read()
    if ret == False: break

    # Redimensionar la imagen para que tenga un ancho de 640
    frame = imutils.resize(frame,width=1080)
    frame = cv2.flip(frame,1)
    frameAux = frame.copy()
    
    cv2.rectangle(frame,(200,5),(1070,600),color_zona1,1)
    cv2.rectangle(frame,(200,5),(550,600),color_zona2,1)
    cv2.rectangle(frame,(740,5),(1070,600),color_zona2,1)
    
    if bg is not None:
        
        # Determinar la región de interés
        ROI = frame[5:600,200:1070]
        grayROI = cv2.cvtColor(ROI,cv2.COLOR_BGR2GRAY)
        
        # Región de interés del fondo de la imagen
        bgROI = bg[5:600,200:1070]
        
        dif = cv2.absdiff(grayROI,bgROI)
        _, th = cv2.threshold(dif, 30, 255, cv2.THRESH_BINARY)
        th = cv2.medianBlur(th, 7)
        
        # Encontrando los contornos de la imagen binaria
        cnts, _ = cv2.findContours(th,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts,key=cv2.contourArea,reverse=True)[:1]
        cv2.drawContours(ROI, cnts, 0, (0,255,0),1)
        
        for cnt in cnts:

            # Encontrar el centro del contorno
            M = cv2.moments(cnt)
            if M["m00"] == 0: M["m00"]=1
            x = int(M["m10"]/M["m00"])
            y = int(M["m01"]/M["m00"])
            cv2.circle(ROI,tuple([x,y]),5,(0,255,0),-1)
            
            # Punto más alto del contorno
            ymin = cnt.min(axis=1)
            cv2.circle(ROI,tuple(ymin[0]),5,color_ymin,-1)
            
            # Contorno encontrado a través de cv2.convexHull
            hull1 = cv2.convexHull(cnt)
            cv2.drawContours(ROI,[hull1],0,color_contorno,2)
            
            # Defectos convexos
            hull2 = cv2.convexHull(cnt,returnPoints=False)
            defects = cv2.convexityDefects(cnt,hull2)
        
        if (x<350): print("izquierda")
        if (x>540): print("derecha")
        if (abs(y-ymin[0][1])>150): print("disparar")
        else: print("no dispirar")

    
    cv2.imshow('Frame',frame)
    
    k = cv2.waitKey(20)
    if k == ord('i'):
        bg = cv2.cvtColor(frameAux,cv2.COLOR_BGR2GRAY)
    if k == 27: break

cap.release()
cv2.destroyAllWindows()
    
    