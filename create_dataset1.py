import numpy as np
from PIL import Image
from PIL import Image, ImageTk
import os, cv2
from datetime import datetime
import json
import tkinter as tk
from tkinter import messagebox
from customtkinter import *
from data_findencodings import coding_face
def capture1(app, name, users, new_user,controller):
    
    path = "./data_faces/" + name + '/'
    detector = cv2.CascadeClassifier("./data/haarcascade_frontalface_default.xml")
    a=False
    keep_processing = True 
    def cap():
        nonlocal a
        global new_img
        try:
            cv2.imwrite(str(path+"/"+new_user["name"]+"_"+new_user["matricule"]+".jpg"), new_img)
            
        except:
            pass
        users.append(new_user)
        coding_face()
        with open("faces.json", "w") as f:
            json.dump(users, f, indent=4)
        a = True
    new_window = tk.Toplevel(app)
    new_window.title("CAMERA")
    new_window.configure(bg="#276678") 
    
    imageLEONI = Image.open("design\OIP41.png")
    photoLEONI = ImageTk.PhotoImage(imageLEONI)
    new_window.iconphoto(False,photoLEONI)
    
    new_window.grid_columnconfigure(0, weight=1)
    new_window.grid_columnconfigure(1, weight=1)

    video_label = tk.Label(new_window,bg="#276678")
    video_label.grid(column=0)
    imageCAP = Image.open("design\capture.png")
    photoCAP = CTkImage(imageCAP,size=(70,70))
    
    button_cap=CTkButton(new_window,text="",corner_radius=50,image=photoCAP,bg_color="#276678",hover_color="#2a572a",command=cap)
    button_cap.grid(column=0)
    
    try:
        os.makedirs(path)
    except:
        pass
    def on_closing():
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ?"):
            vid.release()
            cv2.destroyAllWindows()
            new_window.destroy() 
    
        
        
    
    def main_app10():
        nonlocal detector,a,video_label,keep_processing
        global new_img
        if keep_processing:
            ret, img = vid.read()
            new_img = None
            
            grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face = detector.detectMultiScale(image=grayimg, scaleFactor=1.1, minNeighbors=5)
            for x, y, w, h in face:
                new_img = img[:,:]
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)

            video_label.configure(image=image)
            video_label.image = image
            
            if not a:
                new_window.after(10, main_app10)
            else:
                keep_processing = False
                vid.release()
                cv2.destroyAllWindows()
                new_window.destroy()
                with open("host.csv", "r+") as f:
                    myDataList = f.readlines()
                    name=myDataList[-1].split(',')[0]
                    Matricule=myDataList[-1].split(',')[1].split(',')[0]
                    now = datetime.now()
                    dtString = now.strftime('%Y-%m-%d      %H:%M:%S')
                    f.writelines(f'{name},{Matricule},Admin,Add a user,{dtString} \n')
        
                messagebox.showinfo("SUCCESS", "The modele has been successfully trained!") 
                controller.show_frame_ManageUserPage()
    new_window.protocol("WM_DELETE_WINDOW", on_closing)
    vid = cv2.VideoCapture(0)
    
    main_app10()
    
            
            