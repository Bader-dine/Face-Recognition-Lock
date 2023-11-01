from Detector4 import main_app4
from Detector3 import main_app3

from create_dataset1 import capture1
import tkinter as tk
from tkinter import ttk
from customtkinter import *
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage
import json
import csv
from PIL import Image, ImageTk
import os
from datetime import datetime
names = set()
users = []
services = set()
matricules=set()
listselect=["none","none","none","none"]
with open("Validation.csv", "w") as f:
                    f.writelines(f'False')

def create_empty_json_file(file_path, users):
    try:
        with open(file_path, 'w') as file:
            json.dump([], file)
            users = []
            print("Empty JSON file created successfully.")
    except IOError:
        print("An error occurred while creating the empty JSON file.")


class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global names
        global users
        global services
        global matricules
        global listselect
        services = ["Admin","Process", "Quality", "Maintenance", "Operator"]

        try:
            with open("faces.json", "r") as f:
                users = json.load(f)
            for user in users:
                matricules.add(user["matricule"])
                names.add(user["name"])
        except FileNotFoundError:
            print("JSON file not found. Creating an empty one.")
            create_empty_json_file("faces.json", users)            
        self.title_font = tkfont.Font(family='Helvetica', size=24, weight="bold")
        self.title("Face Recognizer")
        self.resizable(False, False)
        self.attributes('-fullscreen', True)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        size = (width, height)
        x = (width - size[0]) // 2
        y = (height - size[1]) // 2
        self.geometry('{}x{}+{}+{}'.format(*size, x, y))
        
        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        
        # Create the children frame and center it
        children_frame = tk.Frame(self.container, bg='red', width=200, height=200)
        children_frame.grid(row=0, column=0, padx=(width-200)//2, pady=(height-200)//2)
        
        self.frames = {}
        for F in (AdminPage, AddUserPage, MainPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("MainPage")
    def show_frame_MainPageADMIN(self):
        frame = MainPageADMIN(parent=self.container, controller=self)
        frame.configure(bg="#276678") 
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
    def show_frameE(self):
        frame = EditUserPage(parent=self.container, controller=self)
        frame.configure(bg="#276678") 
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
    
    def show_frame_ManageUserPage(self):
        frame = ManageUserPage(parent=self.container, controller=self)
        frame.configure(bg="#276678") 
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.configure(bg="#276678") 
        frame.tkraise()
    

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            self.destroy()


class AdminPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Centering the page
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        buttonNextFont = CTkFont(family='Helvetica', size=20, weight='bold')
        buttonNextFont1 = CTkFont(family='Helvetica', size=30, weight='bold')
        
        self.imageADD = Image.open("design/add user.png")
        self.photoADD = CTkImage(self.imageADD,size=(90,90))
        button1 = CTkButton(self,text="  Add users  ",width=500,height=100,font=buttonNextFont1,image=self.photoADD ,fg_color="#1687A7",hover_color="#2a572a", command=lambda: self.controller.show_frame("AddUserPage"))

        #button1 = tk.Button(self, text="Add a user", height= 4, width=32, font = buttonNextFont, fg="#ffffff", bg="#2a572a",command=lambda: self.controller.show_frame("AddUserPage"))
        
        self.imageMANGER = Image.open("design\MANGER.png")
        self.photoMANGER = CTkImage(self.imageMANGER,size=(90,90))
        button2 = CTkButton(self,text="  Manage users  ",width=500,height=100,font=buttonNextFont1,image=self.photoMANGER ,fg_color="#1687A7",hover_color="#263942", command=lambda: self.controller.show_frame_ManageUserPage())

        #button2 = tk.Button(self, text="Manage users", height= 4, width=32, font = buttonNextFont, fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame_ManageUserPage())
        
        self.imageHOME = Image.open("design/HOME.png")
        self.photoHOME = CTkImage(self.imageHOME,size=(70,70))
        button3 = CTkButton(self,text="    Home Page    ",width=500,height=100,font=buttonNextFont1,image=self.photoHOME ,fg_color="#1687A7",hover_color="#D3E0EA", command=lambda: self.controller.show_frame("MainPage"))
       
        self.imageQ = Image.open("design\Quit.png")
        self.photoQ = CTkImage(self.imageQ,size=(40,40))
        button4 = CTkButton(self,text="Quit ",width=90 ,height=50,font=buttonNextFont,image=self.photoQ ,fg_color="#1687A7",hover_color="#8a3838", command=self.on_closing)
        
        button1.grid(row=0, column=1)
        button2.grid(row=1, column=1)
        button3.grid(row=2, column=1)
        button4.grid(row=3, column=1)
        self.imageLEONI = Image.open("design\OIP4.png")
        resized_image1 = self.imageLEONI.resize((107, 26))
        
        self.photoLEONI = ImageTk.PhotoImage(resized_image1)
        
        tk.Label(self,image=self.photoLEONI, bg="#276678", fg="#F6F5F5").grid(row=4, column=0,pady=(10,10))


    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            self.controller.destroy()


class AddUserPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Centering the page
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        

        self.controller = controller
        self.controller.num_of_images = -1
        
        buttonNextFont = CTkFont(family='Helvetica', size=20, weight='bold')
        tk.Label(self, text="Select a service : ",bg="#276678", fg="#D3E0EA", font='Helvetica 16 bold').grid(row=0, column=0, pady=(10, 10))
        self.menuvar = tk.StringVar(self)
        self.combobox = ttk.Combobox(self, width=66, height=30, textvariable=self.menuvar, values=list(services), state="readonly")
        self.combobox.config(background="lightgrey", font='Helvetica 16')
        self.combobox.grid(row=0, column=1, pady=(10, 10))

        tk.Label(self, text="Enter the name : ",bg="#276678", fg="#D3E0EA", font='Helvetica 16 bold').grid(row=1, column=0, pady=10, padx=5)
        self.user_name =CTkEntry(self,font=buttonNextFont, width=270, height=30)
        self.user_name.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(self, text="Matricule : ",bg="#276678", fg="#D3E0EA", font='Helvetica 16 bold').grid(row=2, column=0, pady=10, padx=5)
        self.matricule = CTkEntry(self,font=buttonNextFont, width=270, height=30)
        
        self.matricule.grid(row=2, column=1, pady=10, padx=10)
        

    
        self.imageb = Image.open("design/back.png")
        self.photob = CTkImage(self.imageb,size=(70,70))
        
        self.buttoncanc= CTkButton(self,text=" Back to settings  ",width=200,height=100,font=buttonNextFont,image=self.photob ,fg_color="#1687A7",hover_color="#D3E0EA", command=lambda: controller.show_frame("AdminPage"))
       
       
        self.buttoncanc.grid(row=4, column=0, pady=(100,0), padx=12)
        
        
        self.imageCAP = Image.open("design\capture.png")
        self.photoCAP = CTkImage(self.imageCAP,size=(70,70))
        
        self.capturebutton= CTkButton(self,text=" Capture Face  ",width=200,height=100,font=buttonNextFont,image=self.photoCAP ,fg_color="#1687A7",hover_color="#D3E0EA", command=self.capimg1)
       
       

        #self.capturebutton = tk.Button(self, text="Capture Face", font=midbutton, height=5, width=28, fg="#ffffff", bg="#2a572a", command=self.capimg1)
        self.capturebutton.grid(row=4, column=2,padx=(10,100), pady=(100,0))

    def capimg1(self):
        if((self.matricule.get() == "" ) or (self.user_name.get()== "" ) or (self.menuvar.get()== "" ) ):
            messagebox.showerror("ERROR", "The user name can't be empty")
            return 0
        
        if self.menuvar.get()!= "Admin" :
            isAdmin = False
        else:
            isAdmin = True
        # Add a new user
        matriculesALL=[]
        for user in users:
                matriculesALL.append(user["matricule"])
        
        
        if matriculesALL.count(self.matricule.get())!=0:
            messagebox.showinfo("ERROR", "matricule exists")
            return 0 
            
        new_user = {
            "name": self.user_name.get(),
            "service": self.menuvar.get(),
            "matricule": self.matricule.get(),
            "isAdmin": isAdmin
        }
        
                    
        
        capture1(app, self.menuvar.get(), users, new_user,self.controller)
    
       
class EditUserPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Centering the page
        global listselect
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.controller = controller
        self.controller.num_of_images = -1
        buttonNextFont = CTkFont(family='Helvetica', size=20, weight='bold')
        tk.Label(self, text="Select a service : ", bg="#276678", fg="#D3E0EA",font='Helvetica 16 bold').grid(row=0, column=0, pady=(10, 10))
        self.menuvar = tk.StringVar(self)
        self.combobox = ttk.Combobox(self, width=66, height=30, textvariable=self.menuvar, values=list(services), state="readonly")
        
        
        self.combobox.config(background="lightgrey", font='Helvetica 16')
        self.combobox.grid(row=0, column=1, pady=(10, 10))

        tk.Label(self, text="Enter the name : ", bg="#276678", fg="#D3E0EA", font='Helvetica 16 bold').grid(row=1, column=0, pady=10, padx=5)
        self.user_name =CTkEntry(self,font=buttonNextFont, width=270, height=30)
        self.user_name.insert(0,listselect[0])
        self.user_name.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(self, text="Matricule : ", bg="#276678", fg="#D3E0EA", font='Helvetica 16 bold').grid(row=2, column=0, pady=10, padx=5)
        self.matricule =CTkEntry(self,font=buttonNextFont, width=270, height=30)
        self.matricule.insert(0,listselect[2])
        self.matricule.grid(row=2, column=1, pady=10, padx=10)

        

        self.imageb = Image.open("design/back.png")
        self.photob = CTkImage(self.imageb,size=(50,50))
        
        self.buttoncanc= CTkButton(self,text=" Back to settings  ",width=250,height=100,font=buttonNextFont,image=self.photob ,fg_color="#1687A7",hover_color="#D3E0EA", command=lambda: self.controller.show_frame_ManageUserPage())
        self.buttoncanc.grid(row=4, column=0, pady=(100,0), padx=12)
        
        self.imagebSA = Image.open("design\save.png")
        self.photobSA = CTkImage(self.imagebSA,size=(70,70))
        
        self.capturebutton = CTkButton(self,text=" SAVE  ",width=250,height=100,font=buttonNextFont,image=self.photobSA ,fg_color="#1687A7",hover_color="#2a572a", command=self.save)
        

        
        self.capturebutton.grid(row=4, column=2,padx=(10,100), pady=(100,0))

    def save(self):
        global listselect
        if((listselect[0] == "none" ) or (listselect[1] == "none" ) or (str(listselect[2]) == "none" ) ):
            messagebox.showerror("SAVE", "Save successfully ")
            self.controller.show_frame_ManageUserPage()
            return 0
        
        
        # Add a new user
        if ((listselect[1] != self.menuvar.get()) and (self.menuvar.get()!= "" )  ):
            service_Edit=self.menuvar.get()
        else:
            service_Edit=listselect[1]
            
        if service_Edit != "Admin" :
            isAdmin = False
        else:
            isAdmin = True 
            
        
        new_user = {
            "name": self.user_name.get(),
            "service": service_Edit,
            "matricule": self.matricule.get(),
            "isAdmin": isAdmin
        }
        ink=0
        for i in users:
            
            if (int(i['matricule']) == listselect[2]):
                break
            ink=ink+1
        if listselect[1]!=service_Edit:
            
            file_path=os.path.join("data_faces/"+ users[ink]["service"]+"/"+users[ink]["name"]+"_"+ users[ink]["matricule"]+".jpg")
            with  Image.open(file_path) as im:
                im.save(os.path.join("data_faces/"+ new_user["service"]+"/"+new_user["name"]+"_"+ new_user["matricule"]+".jpg"))
            os.remove("data_faces//"+ users[ink]["service"]+"//"+users[ink]["name"]+"_"+ users[ink]["matricule"]+".jpg")
        del users[ink]
        
        users.append(new_user)
        with open("faces.json", "w") as f:
            json.dump(users, f, indent=4)
                    
        
        
        with open("host.csv", "r+") as f:
                    myDataList = f.readlines()
                    name=myDataList[-1].split(',')[0]
                    Matricule=myDataList[-1].split(',')[1].split(',')[0]
                    now = datetime.now()
                    dtString = now.strftime('%Y-%m-%d     %H:%M:%S')
                    f.writelines(f'{name},{Matricule},Admin,Edit a user successfully,{dtString} \n')
        
        messagebox.showerror("SAVE", "Save successfully ")
        if new_user:
            
            listselect=[new_user["name"],new_user["service"],new_user["matricule"],new_user["isAdmin"]]
            print(listselect)
        self.controller.show_frame_ManageUserPage()
        
        
# Select a name to detect a face
class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        global matricules
        self.controller = controller
        
        
        
        # Centering the page
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        tk.Label(self, text="Select Your service: ",bg="#276678", fg="#F6F5F5", font='Helvetica 16 bold').grid(row=0, column=0, padx=0, pady=(10, 10))
        # Using a Combobox    466
        self.menuvar = tk.StringVar(self)
    
        self.combobox = ttk.Combobox(self, width=70, height=30, textvariable=self.menuvar, values=list(services), state="readonly")
        self.combobox.config(background="lightgrey", font='Helvetica 16')
        self.combobox.grid(row=0, column=1, padx=0, pady=(10, 10))
        
        
        self.image1 = Image.open("design/admin.png")
        self.photo1 = CTkImage(self.image1,size=(40,40))
        self.buttonext = CTkButton(self,text="",image=self.photo1 ,width=10,height=10,fg_color="#D3E0EA", command=self.goMainADMIN)
        self.buttonext.grid(row=0, column=2, padx=10, pady=(1, 1))
        
        
        image = Image.open("design/sss1.png")
        self.photo = CTkImage(image,size=(300,300))
        self.buttonext = CTkButton(self,text="",corner_radius=50,image=self.photo,bg_color="#1687A7",hover_color="#2a572a", command=self.openwebcam)
        self.buttonext.grid(row=1, column=1, padx=0, pady=(10, 10))
        
        
        self.imageLEONI = Image.open("design\OIP4.png")
        resized_image1 = self.imageLEONI.resize((143, 35))
        self.photoLEONI = ImageTk.PhotoImage(resized_image1)
        tk.Label(self,image=self.photoLEONI, bg="#276678", fg="#F6F5F5").grid(row=2, column=0, padx=0, pady=(10, 10))

    
        
        
        
    
        

    def openwebcam(self):
        name = self.menuvar.get()
        
        
        if name == "" or name is None:
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return 0
        self.controller.active_name = name
        main_app4(app,self.controller.active_name)
        
        
        
        
        
           
    
                

 
    def goMainADMIN(self):
        name = self.menuvar.get()
        with open('faces.json', 'r') as file:
            data = json.load(file) 
            if (len(data) == 0):
                self.controller.show_frame("AdminPage")
                return 0
        if (name == "") or (name is None):
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return 0
        # Check if the user is an Admin
        isAdmin = next((user["isAdmin"] for user in users if user["service"] == name), None)
        if (isAdmin is None) or (isAdmin == False):
            messagebox.showerror("ERROR", "'{}' is not an Admin".format(name))
        else:
            self.controller.active_name = name
            
            main_app3(app,self.controller.active_name,self.controller)

class MainPageADMIN(tk.Frame):
    custom_font = ("Arial", 12, "bold")
    custom_font1 = ("Arial", 10)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        global matricules
        self.controller = controller
        
        # Centering the page
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)
        
        
        frame_left = tk.Frame(self, bg="#276678", width=200, height=400)
        frame_left.pack(side=tk.LEFT)
        

        columns = ('name','Matricule', 'service', 'Activite','Date')
        tree = ttk.Treeview(frame_left, columns=columns, show='headings')
       
        # define headings
        style = ttk.Style(tree)
        style.configure('Treeview',corner_radius=100, font=self.custom_font1, background="#d3d3d3", fieldbackground="#276678", borderwidth=0)
        style.configure('Treeview.Heading', font=self.custom_font, background="#d3d3d3")
        
        
        tree.heading('name', text='Name')
        tree.heading('Matricule', text='Matricule')
        tree.heading('service', text='Service')
        tree.heading('Activite', text='Activite')
        tree.heading('Date', text='Date')
        with open("host.csv", "r") as f:
                red=csv.reader(f)
                
                for face in red:
                    # tree.insert('', tk.END, values=face)
                    row = tree.insert('', tk.END)
                    tree.set(row, 0, face[0])
                    tree.set(row, 1, face[1])
                    tree.set(row, 2, face[2])
                    tree.set(row, 3, face[3])
                    tree.set(row, 4, face[4])
            


        tree.grid(column=0,padx=10,ipady=200, sticky='nsew')

        # add a scrollbar
        
        scrollbar = ttk.Scrollbar(frame_left, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1,ipady=230)
        
        
        
        # Créer le cadre droit
        frame_right = tk.Frame(self, bg="#276678", width=200, height=400)
        frame_right.pack(side=tk.RIGHT)
        
        buttonNextFont = CTkFont(family='Helvetica', size=20, weight='bold')
        
        self.imageHOME = Image.open("design/HOME.png")
        self.photoHOME = CTkImage(self.imageHOME,size=(50,50))
        self.buttonextHOME = CTkButton(frame_right,text="Home Page",width=200,height=60,font=buttonNextFont,image=self.photoHOME ,fg_color="#1687A7",hover_color="#D3E0EA", command=lambda: self.controller.show_frame("MainPage"))
        self.buttonextHOME.grid(row=0, column=0, padx=100, pady=(10, 10))

        self.imageSTT = Image.open("design/1.png")
        self.photoSTT = CTkImage(self.imageSTT,size=(50,50))
        self.buttonextSTT = CTkButton(frame_right,text="  Settings  ",width=200 ,height=60,font=buttonNextFont,image=self.photoSTT ,fg_color="#1687A7",hover_color="#D3E0EA", command=lambda:self.controller.show_frame("AdminPage"))
        self.buttonextSTT.grid(row=1, column=0, padx=100, pady=(30, 30))
        
        self.imageQ = Image.open("design\Quit.png")
        self.photoQ = CTkImage(self.imageQ,size=(40,40))
        self.buttonquit = CTkButton(frame_right,text="Quit ",width=90 ,height=50,font=buttonNextFont,image=self.photoQ ,fg_color="#1687A7",hover_color="#8a3838", command=self.on_closing)
       
        #self.buttonquit = tk.Button(frame_right, text="Quit", height=2, width=12, fg="#263942", bg="#ffffff", command=self.on_closing)
        self.buttonquit.grid(row=2, column=0, padx=150, pady=(50, 50))

        

 
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            self.controller.destroy()

 



class ManageUserPage(tk.Frame):
    custom_font = ("Arial", 12, "bold")
    custom_font1 = ("Arial", 10)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Centering the page
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        global listselect
        
        
        

        self.grid_columnconfigure(0, weight=1)
        
        
        
        
        
        # Open the faces.json file.
        with open('faces.json', 'r') as f:
            faces = json.load(f)

        # Add columns to the Treeview widget.
        frame_TOP = tk.Frame(self, bg="#276678")
        frame_TOP.pack(side=tk.TOP)
        
        columns = ('name', 'service', 'matricule', 'isAdmin')
        tree = ttk.Treeview(frame_TOP, columns=columns, show='headings')
        # define headings
        tree.heading('name', text='Name')
        tree.heading('service', text='Service')
        tree.heading('matricule', text='Matricule')
        tree.heading('isAdmin', text='Admin')
        # Iterate over the faces data and add each row to the Treeview widget.
        style = ttk.Style(tree)
        style.configure('Treeview',corner_radius=100, font=self.custom_font1, background="#d3d3d3", fieldbackground="#276678", borderwidth=0)
        style.configure('Treeview.Heading', font=self.custom_font, background="#d3d3d3")
        for face in faces:
            # tree.insert('', tk.END, values=face)
            row = tree.insert('', tk.END)
            tree.set(row, 0, face['name'])
            tree.set(row, 1, face['service'])
            tree.set(row, 2, face['matricule'])
            tree.set(row, 3, face['isAdmin'])

        tree.grid(row=0, column=0,padx=10,ipady=90,pady=10, sticky='nsew')
        def show_popup_menu(event):
            popup_menu.post(event.x_root, event.y_root)
        
        scrollbar = ttk.Scrollbar(frame_TOP, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1,pady=10, sticky='ns')
        
        def item_select(_):
            global listselect
            
            for i in tree.selection():
                listselect=tree.item(i)["values"]
                
        popup_menu = tk.Menu(self, tearoff=0)
        popup_menu.add_command(label="Edit", command=self.on_Name)
        popup_menu.add_command(label="Delete", command=self.on_Delete)
        popup_menu.add_command(label="Display photo", command=self.Display)
          
        tree.bind("<Button-3>", show_popup_menu)

        tree.bind('<<TreeviewSelect>>',item_select)
        
        # Back Button
        frame_DOWN = tk.Frame(self, bg="#276678")
        frame_DOWN.pack(side=tk.BOTTOM)
        buttonNextFont = CTkFont(family='Helvetica', size=20, weight='bold')
        self.imageb = Image.open("design/back.png")
        self.photob = CTkImage(self.imageb,size=(50,50))
        
        button4= CTkButton(frame_DOWN,text=" Back to settings  ",width=200,height=100,font=buttonNextFont,image=self.photob ,fg_color="#1687A7",hover_color="#D3E0EA", command=lambda: controller.show_frame("AdminPage"))
        
        button4.grid(row=3, column=0, padx=(10, 10), pady=(10, 10))
        try:
            self.imageNAME = Image.open("data_faces//"+ listselect[1]+"//"+listselect[0]+"_"+ str(listselect[2])+".jpg")
            resized_imageNAME = self.imageNAME.resize((400, 300))
            
            self.photoNAME = ImageTk.PhotoImage(resized_imageNAME)
            
            self.ii=tk.Label(frame_DOWN,image=self.photoNAME, bg="#276678", fg="#F6F5F5")
            
            self.ii.grid(row=3, column=1, pady=(10,10))
        except FileNotFoundError:
            listselect=["none","none","none","none"]
            self.imageNAME = Image.open("data_faces//"+ listselect[1]+"//"+listselect[0]+"_"+ str(listselect[2])+".jpg")
            resized_imageNAME = self.imageNAME.resize((400, 300))
            
            self.photoNAME = ImageTk.PhotoImage(resized_imageNAME)
            
            self.ii=tk.Label(frame_DOWN,image=self.photoNAME, bg="#276678", fg="#F6F5F5")
            
            self.ii.grid(row=3, column=1, pady=(10,10))
            
    def Display(self):
        self.controller.show_frame_ManageUserPage()
        
      
    def on_Name(self):
        self.controller.show_frameE()
    def on_Delete(self):
        rep=messagebox.askyesno("Delete Confimation","are you sure you want delete this user")
        if rep:
            ink=0
            for i in users:
                
                if(int(i["matricule"])==listselect[2]):
                    break
                ink =ink+1
            
            
            os.remove("data_faces//"+ users[ink]["service"]+"//"+users[ink]["name"]+"_"+ users[ink]["matricule"]+".jpg")
            os.remove("data_faces_coding//"+ users[ink]["service"]+"//"+users[ink]["name"]+"_"+ users[ink]["matricule"]+".txt")
            del users[ink]
            with open("faces.json", "w") as f:
                json.dump(users, f, indent=4)
            
            with open("host.csv", "r+") as f:
                    myDataList = f.readlines()
                    name=myDataList[-1].split(',')[0]
                    Matricule=myDataList[-1].split(',')[1].split(',')[0]
                    now = datetime.now()
                    dtString = now.strftime('%Y-%m-%d      %H:%M:%S')
                    f.writelines(f'{name},{Matricule},Admin,deleted successfully!,{dtString} \n')

                    
            self.controller.show_frame_ManageUserPage()
        else:
            return 0
            


app = MainUI()
imageLEONI = Image.open("design\OIP41.png")
photoLEONI = ImageTk.PhotoImage(imageLEONI)
app.iconphoto(False,photoLEONI)
app.mainloop()

