import cv2
from tkinter import messagebox
import json
from PIL import Image, ImageTk
import tkinter as tk
import numpy as np
import face_recognition
import os
from datetime import datetime
from test import test


def main_app3(app,name,controller):
    
    new_window = tk.Toplevel(app)
    new_window.title("CAMERA")
    imageLEONI = Image.open("design\OIP41.png")
    photoLEONI = ImageTk.PhotoImage(imageLEONI)
    new_window.iconphoto(False,photoLEONI)

    path = "data_faces_coding//" + name
    images = []
    names = []
    bases = []
    
    setname = set()
    classNames = []
    

    myList = os.listdir(path)

    for cl in myList:
        with open(f'{path}/{cl}', "r+") as f:
            encoded_list = json.loads(f.read())
            curImg = np.array(encoded_list)
            images.append(curImg)
        classNames.append(cl.split('_')[0])
        base = [cl.split('_')[0], cl.split('_')[1].split('.')[0]]
        bases.append(base)

    encodeListKnown = images
    time_val = 0
    ST = 0
    a=False
    list_fake=[]
    keep_processing = True 

    video_label = tk.Label(new_window)
    video_label.pack()
    def on_closing():
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ?"):
            video_capture.release()
            cv2.destroyAllWindows()
            new_window.destroy() 
    
    
    def main_app10():
        nonlocal time_val, ST,names,classNames,a,setname,video_capture,video_label,keep_processing,list_fake
        if keep_processing:
        
        
            success, img = video_capture.read()
    
            
            
            img = cv2.resize(img, (0, 0), None, 1, 1)
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            
            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
            
            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace,tolerance=0.49)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]and (faceDis[matchIndex]>0.20):
                    res_face=test(img,"fakeface/resources/anti_spoof_models",3)
                    list_fake.append(res_face)      
                    name1 = classNames[matchIndex].upper()
                    name2 = classNames[matchIndex]
                    
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name1, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    if res_face==2:
                        cv2.putText(img, 'Fake', (x1 + 110, y1 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    else:
                        cv2.putText(img, 'Real', (x1 + 110, y1 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    
                    names.append(name2)
                    setname = set(names)
                    if time_val == 0:
                        now = datetime.now()
                        s = now.strftime('%S')
                        s1 = now.strftime('%M')
                        ST = int(s1) * 60 + int(s)
                        time_val = 1
                    now = datetime.now()
                    s2 = now.strftime('%S')
                    s3 = now.strftime('%M')
                    ST1 = int(s3) * 60 + int(s2)
                    
                    if ST1 - ST > 8:
                        ST = ST1
                        names = []
                        list_fake=[]
                        break
                    
                    for i in setname:
                        if (names.count(i) > 6) and (ST1 - ST >= 5) and ((len(list_fake)-list_fake.count(2))>4):
                            for j in bases:
                                if j[0] == name2:
                                    a = True
                                    
                                    
                                    
                                    if a:
                                        Matricule = j[1]
                                        Namematricule=j[0]
                                        with open("host.csv", "r+") as f:
                                                myDataList = f.readlines()
                                                now = datetime.now()
                                                dtString = now.strftime('%Y-%m-%d      %H:%M:%S')
                                                f.writelines(f'{Namematricule},{Matricule},{name},go to page admin,{dtString} \n')
                
                                        controller.show_frame_MainPageADMIN()
                                    
            

            image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)

            video_label.configure(image=image)
            video_label.image = image
            
            if not a:
                new_window.after(10, main_app10)
            else:
                keep_processing = False 
                video_capture.release()
                cv2.destroyAllWindows()
                new_window.destroy()
    new_window.protocol("WM_DELETE_WINDOW", on_closing)
    video_capture = cv2.VideoCapture(0)
    
    main_app10()
    
   

# You can call the main_app4 function with the necessary parameters
# main_app4(app, name)

      