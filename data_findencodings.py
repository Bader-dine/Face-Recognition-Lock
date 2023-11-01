import cv2
import numpy as np
import face_recognition
import os


def coding_face():
    services = ["Admin","Process", "Quality", "Maintenance", "Operator"]
    for name in services:
    

            
        path = "data_faces_coding//"+ name
        path1 = "data_faces//"+ name
        images = []
        
        bases=[]
        
        classNames = []
        myList = os.listdir(path1)
        
        for cl in myList:
            curImg = cv2.imread(f'{path1}/{cl}')
            images.append(curImg)
            classNames.append(cl.split('_')[0])
            base=[cl.split('_')[0],cl.split('_')[1].split('.')[0]]
            bases.append(base)
        
        
        
        
        idx=0
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encoded_string = np.array2string(encode, separator=', ')
            with open(path+"//"+bases[idx][0]+"_"+bases[idx][1]+".txt", "w") as f:
                f.write(encoded_string)
            idx=idx+1
            
            
        
        
        

        

    