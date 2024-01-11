import cv2 # Importă biblioteca OpenCV pentru prelucrarea imaginilor și a videoclipurilor.
import numpy as np #Importă biblioteca NumPy pentru manipularea eficientă a matricelor și a operatiilor pe acestea.
def nothing(x): #Defineste o funcție goală. Aceasta va fi utilizată mai târziu ca funcție de callback pentru bara de track.
    pass
img=cv2.VideoCapture(0) # Inițializează un obiect VideoCapture pentru a captura fluxul video de la camera web (dispozitivul cu indexul 0).
cv2.namedWindow("Trackbars")  #Creează o fereastră pentru bara de track.
cv2.createTrackbar("L-H", "Trackbars",0, 255,nothing) #Creează o bara de track numită "L-H" în fereastra "Trackbars", cu valori între 0 și 255, și utilizează funcția nothing ca funcție de callback.
cv2.createTrackbar("U-S", "Trackbars",0, 255,nothing) #Creează o bara de track numită "U-S" în fereastra "Trackbars", cu valori între 0 și 255, și utilizează funcția nothing ca funcție de callback.
ret, frame1=img.read() #Capturează prima imagine din fluxul video.
while(True): # Intră în bucla infinită pentru a prelucra continuu fluxul video.
    ret, frame1=img.read() #Captureaza o nouă imagine din fluxul video.
    frame1 = cv2.flip(frame1, 1) # 1 indică oglindirea pe orizontală (axa Y)
    l_h = cv2.getTrackbarPos("L-H", "Trackbars") #Obține poziția barei de track "L-H".
    u_s = cv2.getTrackbarPos("U-S", "Trackbars") #Obține poziția barei de track "U-S".
    imgGrey=cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY) # Converteste imaginea color la scala de gri.
    _,thrash=cv2.threshold(imgGrey, l_h, u_s,cv2.THRESH_BINARY)  #Aplică o pragizare binară pe imaginea în scala de gri în funcție de valorile setate de barele de track.
    contours,_=cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        approx=cv2.approxPolyDP(contour, 0.1* cv2.arcLength(contour, True), True) #Aproximează conturul pentru a reduce numărul de puncte.
        if (cv2.contourArea(contour)>1000 and cv2.contourArea(contour)<30000 and len(approx)>2): #Verifică condiții pentru a decide dacă conturul reprezintă un obiect valid.
            cv2.drawContours(frame1, [approx], 0, (0,0,255), 8) # Desenează conturul pe imaginea originală.
            x=approx.ravel()[0] #Obține coordonatele x și y ale primului punct al conturului.
            y=approx.ravel()[1] #Obține coordonatele x și y ale primului punct al conturului.
            if(len(approx)==3): #Verifică dacă conturul are 3 laturi (triunghi).
                cv2.putText(frame1, 'Triunghi', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (102, 255, 51), 5, cv2.LINE_AA) #Adaugă textul "Triunghi" în imaginea originală.
            elif(len(approx)==4): #Verifică dacă conturul are 4 laturi (posibil patrat sau dreptunghi).
                x ,y, w, h = cv2.boundingRect(approx) #Obține coordonatele și dimensiunile dreptunghiului delimitator al conturului.
                aspectRatio = float(w)/float(h) #Calculează raportul de aspect al dreptunghiului.
                if aspectRatio >= 0.8 and aspectRatio <= 1.2: #Verifică dacă raportul de aspect indică că dreptunghiul este aproape pătrat.
                    cv2.putText(frame1, 'Patrat', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (204, 0, 0), 5, cv2.LINE_AA) #Adaugă textul "Patrat" în imaginea originală.
                else:
                    cv2.putText(frame1, 'Dreptunghi', (x, y), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 255), 5, cv2.LINE_AA) #Dacă nu este un pătrat, adaugă textul "Dreptunghi" în imaginea originală.
    cv2.imshow('video', frame1) #Afișează imaginea originală cu contururile detectate.3
    cv2.imshow('vid', thrash) # Afișează imaginea binară rezultată după pragizare.
    ret, frame1 = img.read() #Captureaza o nouă imagine din fluxul video.
    if(cv2.waitKey(1) & 0xFF == ord('q')): #Verifică apăsarea tastei 'q'. Dacă da, întrerupe bucla.
        break


cv2.destroyAllWindows() #Distruge toate ferestrele deschise.




