from tkinter import *
import customtkinter
import tkinter
import customtkinter
from PIL import Image
from tkinter import filedialog as fd 
from  CTkMessagebox import  CTkMessagebox
from secret_audio import extractAudio, encode, decode, Create_Keys

 
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

class App(customtkinter.CTk):
    frames = {"frame1": None, "frame2": None, "frame3":None}
    def frame1_selector(self):
        App.frames["frame2"].pack_forget()
        App.frames["frame3"].pack_forget()
        App.frames["frame1"].pack(in_=self.right_side_container,side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)
    def frame2_selector(self):
        App.frames["frame1"].pack_forget()
        App.frames["frame3"].pack_forget()
        App.frames["frame2"].pack(in_=self.right_side_container,side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)
    def frame3_selector(self):
        App.frames["frame1"].pack_forget()
        App.frames["frame2"].pack_forget()
        App.frames["frame3"].pack(in_=self.right_side_container,side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)
    def paste_file_name(self):    #the function called to open up the file dialog 
        self.file_name = fd.askopenfilename()
        self.entry_audio.set(self.file_name)
    def paste_file_name_out(self):    #the function called to open up the file dialog 
        self.file_name = fd.askopenfilename()
        self.output_audio.set(self.file_name)
    def paste_pukey_name(self):    #the function called to open up the file dialog 
        self.file_name = fd.askopenfilename()
        self.entry_pukey.set(self.file_name)
    def paste_prkey_name(self):    #the function called to open up the file dialog 
        self.file_name = fd.askopenfilename()
        self.entry_prkey.set(self.file_name)
    def run_encode(self):
        try:
            self.input_for_encode = [self.ytentry_frame2.get(),self.entry_audio.get()]
            if len(list(filter(None, self.input_for_encode))) == 2:
                CTkMessagebox(self.main_container,height = 20,title="Error", message="Please only choose one audio input!", icon="cancel")
            elif len(list(filter(None, self.input_for_encode))) == 0 :
                CTkMessagebox(self.main_container,height = 20,title="Error", message="Please choose one audio input!", icon="cancel")
            elif len(self.entry_pukey.get()) == 0 :
                CTkMessagebox(self.main_container,height = 20,title="Error", message="Please select your public key!", icon="cancel")
            elif self.entry_pukey.get().endswith('.pem') != True:
                CTkMessagebox(self.main_container,height = 20,title="Error", message="Please use a valid public key!", icon="cancel")
            elif len(self.msgentry_frame2.get()) == 0 :
                CTkMessagebox(self.main_container,height = 20,title="Error", message="Write a message to encode!", icon="cancel")
            elif len(self.outentry_frame2.get()) == 0 :
                CTkMessagebox(self.main_container,height = 20,title="Error", message="Write a name for the Output file!", icon="cancel")
            elif self.input_for_encode.index(''.join(list(filter(None, self.input_for_encode)))) == 0:
                if self.ytentry_frame2.get().startswith('https://www.youtube.com/watch') != True:
                    CTkMessagebox(self.main_container,height = 20,title="Error", message="Please write a valid URL!", icon="cancel")
                else:
                    extractAudio(self.ytentry_frame2.get(),'yt_input')
                    encode('yt_input.wav',self.msgentry_frame2.get(),self.entry_pukey.get(),self.outentry_frame2.get())  
                    CTkMessagebox(self.main_container,height = 20,title="Encoded Message", message="Your output audio file is on your folder")
            else:
                if self.entry_audio.get().endswith('.wav') != True:
                    CTkMessagebox(self.main_container,height = 20,title="Error", message="This program only supports .wav files", icon="cancel")
                else:
                    encode(self.entry_audio.get(),self.msgentry_frame2.get(),self.entry_pukey.get(),self.outentry_frame2.get())
                    CTkMessagebox(self.main_container,height = 20,title="Encoded Message", message="Your output audio file is on your folder")
        except BaseException as e:
            CTkMessagebox(self.main_container,height = 20,title="Error", message=e, icon="cancel")
    def run_decode(self):
        try:
            if len(self.output_audio.get()) == 0:
                CTkMessagebox(self.main_container,height = 20,title="Error", message="Please select an audio file!", icon="cancel")
            elif len(self.prkey_entry_frame3.get()) == 0 :
                CTkMessagebox(self.main_container,height = 20,title="Error", message="Please select your private key!", icon="cancel")
            elif self.output_audio.get().endswith('.wav') != True:
                CTkMessagebox(self.main_container,height = 20,title="Error", message="This program only supports .wav files", icon="cancel")
            elif self.prkey_entry_frame3.get().endswith('.pem') != True:
                CTkMessagebox(self.main_container,height = 20,title="Error", message="Please use a valid private key!", icon="cancel")
            else:
                msg = decode(self.output_audio.get(),self.prkey_entry_frame3.get())
                CTkMessagebox(self.main_container,height = 20,title="Decoded Message", message=msg)

        except BaseException as e:
            CTkMessagebox(self.main_container,height = 20,title="Error", message=e, icon="cancel")
    
        
                    
    
    def __init__(self):
        super().__init__()
        self.title("Secure Audio Encoding")
        self.geometry("{0}x{0}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.key_image= customtkinter.CTkImage(Image.open('input_image/lock.png'), size=(26, 26))
        self.encode_image= customtkinter.CTkImage(Image.open('input_image/encode.png'), size=(26, 26))
        self.decode_image= customtkinter.CTkImage(Image.open('input_image/decode.png'), size=(26, 26))
        self.logo_image = customtkinter.CTkImage(Image.open('input_image/logo.png'), size=(26, 26))
        self.logo_welcome = customtkinter.CTkImage(Image.open('input_image/logo.png'), size=(120, 120))
        self.wm_iconbitmap('input_image/logo.ico')
        # contains everything
        self.main_container = customtkinter.CTkFrame(self)
        self.main_container.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)
        # left side panel -> for frame selection
        left_side_panel = customtkinter.CTkFrame(self.main_container, width=250)
        left_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=FALSE,  padx=30, pady=10)
        #Label
        navigation_frame_label = customtkinter.CTkLabel(left_side_panel, text="  Secure Audio Encoding", image=self.logo_image,compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        # buttons to select the frames
        bt_frame1 = customtkinter.CTkButton(left_side_panel, corner_radius=8, height=40, border_spacing=10, text="Create Keys",fg_color="green", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=self.key_image, anchor="w", command=self.frame1_selector)
        bt_frame1.place(relx = 0.5, rely = 0.12, anchor = CENTER)
        bt_frame2 = customtkinter.CTkButton(left_side_panel, corner_radius=8, height=40, border_spacing=10, text="Encode Message",fg_color="green", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=self.encode_image, anchor="w", command=self.frame2_selector)
        bt_frame2.place(relx = 0.5, rely = 0.24, anchor = CENTER)
        bt_frame3 = customtkinter.CTkButton(left_side_panel, corner_radius=8, height=40, border_spacing=10, text="Decode Message",fg_color="green", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=self.decode_image, anchor="w", command=self.frame3_selector)
        bt_frame3.place(relx = 0.5, rely = 0.36, anchor = CENTER)
        # right side panel -> to show the frame1 or frame 2
        self.right_side_panel = customtkinter.CTkFrame(self.main_container)
        self.right_side_panel.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=10, pady=10)
        self.right_side_container = customtkinter.CTkFrame(self.right_side_panel)
        self.right_side_container.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=0, pady=0)
        self.welcome_label = customtkinter.CTkLabel(self.right_side_container, text="  Secure Audio Encoding", image=self.logo_welcome,compound="left", font=customtkinter.CTkFont(size=60, weight="bold"))
        self.welcome_label.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
        self.welcome_text = customtkinter.CTkTextbox(self.right_side_container, width=550, corner_radius=5,fg_color = 'transparent', font = customtkinter.CTkFont(size=25, slant="italic"))
        self.welcome_text.place(relx=0.65, rely=0.58, anchor=tkinter.CENTER)
        self.welcome_text.insert("0.0","Keeping secrets safe")
        ##Create Keys
        App.frames['frame1'] = customtkinter.CTkFrame(self.main_container)
        my_font = customtkinter.CTkFont(family="Times Bold", size=18, weight='bold')
        self.textbox = customtkinter.CTkTextbox(App.frames['frame1'], width=550, corner_radius=5,fg_color = 'transparent', font = (my_font,18))
        self.textbox.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
        self.textbox.insert("0.0","When you click button 'Run', two new files will appear in your folder. \n\n'Public_key.pem' file will be used to encode messages. \n'Private_key.pem' will be used to decode audio files. \n\nYou can change the names to whatever convention you may like,\nremembering which is the public and private key.")
        bt_from_frame1 = customtkinter.CTkButton(App.frames['frame1'], text="Run", command=lambda:Create_Keys() )
        bt_from_frame1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        ##Encode Message Frame
        App.frames['frame2'] = customtkinter.CTkFrame(self.main_container)
        #Youtube Entry frame and label
        ytentry_label_frame2 = customtkinter.CTkLabel(App.frames['frame2'], text="Insert Youtube URL:", anchor="w")
        ytentry_label_frame2.place(relx=0.05, rely=0.10,anchor=tkinter.NW)
        self.ytentry_frame2 = customtkinter.CTkEntry(App.frames['frame2'], placeholder_text="Insert Youtube URL...",width=450,height=25,border_width=1,corner_radius=5)
        self.ytentry_frame2.place(relx=0.05, rely=0.15, anchor=tkinter.NW)
        or_label_frame2 = customtkinter.CTkLabel(App.frames['frame2'], text="OR", anchor="w")
        or_label_frame2.place(relx=0.45, rely=0.15,anchor=tkinter.NW)
        #Select Audio File frame and label
        self.entry_audio = tkinter.StringVar()
        auentry_label_frame2 = customtkinter.CTkLabel(App.frames['frame2'], text="Select your own audio:", anchor="w")
        auentry_label_frame2.place(relx=0.49, rely=0.10,anchor=tkinter.NW)
        self.auentry_frame2 = customtkinter.CTkEntry(App.frames['frame2'], textvariable=self.entry_audio,width=400,height=25,border_width=1,corner_radius=5)
        self.auentry_frame2.place(relx=0.49, rely=0.15, anchor=tkinter.NW)
        #Select file button
        bt_selfile = customtkinter.CTkButton(App.frames['frame2'], text="Search", command=lambda: self.paste_file_name() ,width= 35)
        bt_selfile.place(relx=0.86, rely=0.164, anchor=tkinter.CENTER)
        #Select your Public Key
        self.entry_pukey = tkinter.StringVar()
        pukey_entry_label_frame2 = customtkinter.CTkLabel(App.frames['frame2'], text="Select your public key:", anchor="w")
        pukey_entry_label_frame2.place(relx=0.05, rely=0.20,anchor=tkinter.NW)
        pukey_entry_frame2 = customtkinter.CTkEntry(App.frames['frame2'], textvariable=self.entry_pukey,width=450,height=25,border_width=1,corner_radius=5)
        pukey_entry_frame2.place(relx=0.05, rely=0.25, anchor=tkinter.NW)
        #Select key button
        pukey_bt_selfile = customtkinter.CTkButton(App.frames['frame2'], text="Search", command=lambda: self.paste_pukey_name() ,width= 35)
        pukey_bt_selfile.place(relx=0.46, rely=0.264, anchor=tkinter.CENTER)
        #Insert Message to encode
        msgentry_label_frame2 = customtkinter.CTkLabel(App.frames['frame2'], text="Insert message to encode:", anchor="w")
        msgentry_label_frame2.place(relx=0.05, rely=0.30,anchor=tkinter.NW)
        self.msgentry_frame2 = customtkinter.CTkEntry(App.frames['frame2'], placeholder_text="Write your message...",width=922,height=25,border_width=1,corner_radius=5)
        self.msgentry_frame2.place(relx=0.05, rely=0.35, anchor=tkinter.NW)
        #Insert Name of output audio
        outentry_label_frame2 = customtkinter.CTkLabel(App.frames['frame2'], text="Insert a name for the output audio:", anchor="w")
        outentry_label_frame2.place(relx=0.05, rely=0.40,anchor=tkinter.NW)
        self.outentry_frame2 = customtkinter.CTkEntry(App.frames['frame2'], placeholder_text="Output name...",width=922,height=25,border_width=1,corner_radius=5)
        self.outentry_frame2.place(relx=0.05, rely=0.45, anchor=tkinter.NW)
        #Run Button
        bt_from_frame2 = customtkinter.CTkButton(App.frames['frame2'], text="Run", command=lambda:self.run_encode() )
        bt_from_frame2.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)

        ##Decode Message Frame
        App.frames['frame3'] = customtkinter.CTkFrame(self.main_container)
        #Select Audio File frame and label
        self.output_audio = tkinter.StringVar()
        auoutput_label_frame3 = customtkinter.CTkLabel(App.frames['frame3'], text="Select audio to decode:", anchor="w")
        auoutput_label_frame3.place(relx=0.05, rely=0.10,anchor=tkinter.NW)
        auoutput_frame2 = customtkinter.CTkEntry(App.frames['frame3'], textvariable=self.output_audio,width=450,height=25,border_width=1,corner_radius=5)
        auoutput_frame2.place(relx=0.05, rely=0.15, anchor=tkinter.NW)
        #Select file button
        bt_selfile_out = customtkinter.CTkButton(App.frames['frame3'], text="Search", command=lambda: self.paste_file_name_out() ,width= 50)
        bt_selfile_out.place(relx=0.46, rely=0.164, anchor=tkinter.CENTER)
        #Select your Private Key
        self.entry_prkey = tkinter.StringVar()
        prkey_entry_label_frame3 = customtkinter.CTkLabel(App.frames['frame3'], text="Select your private key:", anchor="w")
        prkey_entry_label_frame3.place(relx=0.05, rely=0.20,anchor=tkinter.NW)
        self.prkey_entry_frame3 = customtkinter.CTkEntry(App.frames['frame3'], textvariable=self.entry_prkey,width=450,height=25,border_width=1,corner_radius=5)
        self.prkey_entry_frame3.place(relx=0.05, rely=0.25, anchor=tkinter.NW)
        #Select key button
        prkey_bt_selfile = customtkinter.CTkButton(App.frames['frame3'], text="Search", command=lambda: self.paste_prkey_name() ,width= 35)
        prkey_bt_selfile.place(relx=0.46, rely=0.264, anchor=tkinter.CENTER)
        #Run Button
        bt_from_frame3 = customtkinter.CTkButton(App.frames['frame3'], text="Run", command=lambda:self.run_decode() )
        bt_from_frame3.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)

    

a = App()
a.mainloop()