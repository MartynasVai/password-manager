import tkinter as tk
from tkinter import messagebox
from tkinter import font
import tkinter as tk
import time
import pyperclip
import pyautogui
from tkcalendar import DateEntry
from tkinter import ttk
from managedata import Managedata
from encryption import Encryption
import secrets
import string

class Main(tk.Frame):
    def __init__(self, root):

        self.root = root 
        root.bind('<FocusOut>', self.on_focus_out)
        new_font = font.Font(family="Montserrat", size=10, weight="bold")
        root.option_add("*Font", new_font)
        root.option_add("*Frame.background", "#313338")
        root.option_add("*Label.background", "#313338")
        root.option_add("*Button.background", "#313338")
        root.option_add("*Checkbutton.background", "#313338")
        root.option_add("*Label.foreground", "white")
        root.option_add("*Button.foreground", "white")
        self.root.geometry('1000x500')
        self.data_manager = Managedata()
        self.encryption = Encryption()
        self.selected_item=None
        self.selected_reminder=None
        self.write_flag = False
        
        


# Register form-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.register_frame = tk.Frame(self.root)
        #self.register_frame.grid(row=0, column=0, padx=10, pady=5)
        #self.register_frame.grid_remove()

        self.register_username_label = tk.Label(self.register_frame, text="Vartotojo vardas:")
        self.register_username_entry = tk.Entry(self.register_frame)

        self.register_email_label = tk.Label(self.register_frame, text="El. paštas:")
        self.register_email_entry = tk.Entry(self.register_frame)

        self.register_password_label = tk.Label(self.register_frame, text="Slaptažodis:")
        self.register_password_entry = tk.Entry(self.register_frame, show="*")

        self.register_password2_label = tk.Label(self.register_frame, text="Pakartoti slaptažodį:")
        self.register_password2_entry = tk.Entry(self.register_frame, show="*")

        self.register_button = tk.Button(self.register_frame, text="Registracija",command=self.register)#, command=self.register_user
        self.go_to_login_button = tk.Button(self.register_frame, text="Prisijungimas", command=self.show_login_form)#, command=self.show_login_form

        # Grid layout for register form
        self.register_username_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.register_username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.register_email_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.register_email_entry.grid(row=1, column=1, padx=10, pady=5)

        self.register_password_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.register_password_entry.grid(row=2, column=1, padx=10, pady=5)

        self.register_password2_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.register_password2_entry.grid(row=3, column=1, padx=10, pady=5)

        self.register_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.go_to_login_button.grid(row=5, column=0, columnspan=2, pady=10)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # Login form---------------------------------------------------------------------------
        self.login_frame = tk.Frame(root)
        #self.login_frame.grid(row=0, column=0, padx=10, pady=5)
        #self.login_frame.grid_remove()

        self.login_username_label = tk.Label(self.login_frame, text="Vartotojo vardas:")
        self.login_username_entry = tk.Entry(self.login_frame)

        self.login_password_label = tk.Label(self.login_frame, text="Slaptažodis:")
        self.login_password_entry = tk.Entry(self.login_frame, show="*")

        self.login_button = tk.Button(self.login_frame, text="Prisijungti", command=self.login)#_user
        self.go_to_register_button = tk.Button(self.login_frame, text="Registracija", command=self.show_register_form)

        # Grid layout for login form
        self.login_username_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.login_username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.login_password_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.login_password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)
        self.go_to_register_button.grid(row=3, column=0, columnspan=2, pady=10)
#---------------------------------------------------------------------------------------------------------------
        #TOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAME
        self.top_frame = tk.Frame(root)

        # Greyed out section on the left
        self.button0 = tk.Button(self.top_frame, text="Slaptažodžių valdymas", padx=0, pady=0, width=50, command=self.show_password_manager_frame)
        self.button0.grid(row=0, column=0, sticky="new")

        # Button in the middle
        self.button1 = tk.Button(self.top_frame, text="Paskyros valdymas", padx=0, pady=0, width=50, command=self.show_account_manager_frame)#,command=main_instance.top2_button
        self.button1.grid(row=0, column=1, sticky="new")

        # Button in the right
        self.button2 = tk.Button(self.top_frame, text="Priminimų valdymas", padx=0, pady=0, width=50,command=self.show_reminder_manager_frame)#,command=main_instance.top3_button
        self.button2.grid(row=0, column=2, sticky="new")

        for i in range(3):
            self.top_frame.grid_columnconfigure(i, weight=1)

#TOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAMETOPFRAME
#--------------CREATE PASSWORD
        self.create_pwd_frame = tk.Frame(root)

        self.create_pwd_label1 = tk.Label(self.create_pwd_frame, text="Pavadinimas:")
        self.create_pwd_label1.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.create_pwd_entry1 = tk.Entry(self.create_pwd_frame)
        self.create_pwd_entry1.grid(row=2, column=0, padx=10, pady=5)


        self.create_pwd_label2 = tk.Label(self.create_pwd_frame, text="Vartotojo vardas:")
        self.create_pwd_label2.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        self.create_pwd_entry2 = tk.Entry(self.create_pwd_frame)
        self.create_pwd_entry2.grid(row=4, column=0, padx=10, pady=5)


        self.create_pwd_label3 = tk.Label(self.create_pwd_frame, text="El. paštas:")
        self.create_pwd_label3.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

        self.create_pwd_entry3 = tk.Entry(self.create_pwd_frame)
        self.create_pwd_entry3.grid(row=6, column=0, padx=10, pady=5)


        self.create_pwd_label4 = tk.Label(self.create_pwd_frame, text="Slaptažodis:")
        self.create_pwd_label4.grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)

        self.create_pwd_entry4 = tk.Entry(self.create_pwd_frame)
        self.create_pwd_entry4.grid(row=8, column=0, padx=10, pady=5)

        self.create_pwd_button = tk.Button(self.create_pwd_frame, text="Kurti", command=self.create)
        self.create_pwd_button.grid(row=9, column=0, columnspan=2, pady=10)


#EDIT PASSWORD---------------------------------------------------
        self.edit_pwdframe = tk.Frame(root)

        self.edit_pwdlabel1 = tk.Label(self.edit_pwdframe, text="Pavadinimas:")
        self.edit_pwdlabel1.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.edit_pwdentry1 = tk.Entry(self.edit_pwdframe)
        self.edit_pwdentry1.grid(row=2, column=0, padx=10, pady=5)
        self.edit_pwdentry1.insert(0, "text")


        self.edit_pwdlabel2 = tk.Label(self.edit_pwdframe, text="Vartotojo vardas:")
        self.edit_pwdlabel2.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.edit_pwdentry1.insert(0, "")

        self.edit_pwdentry2 = tk.Entry(self.edit_pwdframe)
        self.edit_pwdentry2.grid(row=4, column=0, padx=10, pady=5)


        self.edit_pwdlabel3 = tk.Label(self.edit_pwdframe, text="El. paštas:")
        self.edit_pwdlabel3.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

        self.edit_pwdentry3 = tk.Entry(self.edit_pwdframe)
        self.edit_pwdentry3.grid(row=6, column=0, padx=10, pady=5)


        self.edit_pwdlabel4 = tk.Label(self.edit_pwdframe, text="Slaptažodis:")
        self.edit_pwdlabel4.grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)

        self.edit_pwdentry4 = tk.Entry(self.edit_pwdframe)
        self.edit_pwdentry4.grid(row=8, column=0, padx=10, pady=5)

        self.edit_pwdbutton = tk.Button(self.edit_pwdframe, text="Redaguoti",command=self.edit)
        self.edit_pwdbutton.grid(row=9, column=0, columnspan=2, pady=10)

#GENERATE PASSWORD---------------------------------------------------------------------------------------------------------------
        self.generate_password_frame = tk.Frame(root)

        self.generate_password_label1 = tk.Label(self.generate_password_frame, text="Slaptažodis:")
        self.generate_password_label1.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.generate_password_entry1 = tk.Entry(self.generate_password_frame)
        self.generate_password_entry1.grid(row=2, column=0, padx=10, pady=5, columnspan=2,sticky="new")


        self.generate_pwd_button = tk.Button(self.generate_password_frame, text="Generuoti",command=self.generate_password)
        self.generate_pwd_button.grid(row=9, column=0, columnspan=2, pady=10)

        for i in range(2):
            self.generate_password_frame.grid_columnconfigure(i, weight=1)
#FILL PASSWORD-------------------------------------------------------------------------------------------------------------------
        self.fill_pwdframe = tk.Frame(root)

        self.fill_pwdlabel1 = tk.Label(self.fill_pwdframe, text="Pavadinimas:")
        self.fill_pwdlabel1.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.fill_pwdentry1 = tk.Entry(self.fill_pwdframe)
        self.fill_pwdentry1.grid(row=2, column=0, padx=10, pady=5)
        self.fill_pwdentry1.insert(0, "text")

        self.fill_pwdbutton1 = tk.Button(self.fill_pwdframe, text="Pildyti pavadinimą",command=lambda: self.fill(1))
        self.fill_pwdbutton1.grid(row=2, column=1, pady=10)

        self.fill_pwdlabel2 = tk.Label(self.fill_pwdframe, text="Vartotojo vardas:")
        self.fill_pwdlabel2.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.fill_pwdentry1.insert(0, "")

        self.fill_pwdentry2 = tk.Entry(self.fill_pwdframe)
        self.fill_pwdentry2.grid(row=4, column=0, padx=10, pady=5)

        self.fill_pwdbutton2 = tk.Button(self.fill_pwdframe, text="Pildyti vartotojo vardą",command=lambda: self.fill(2))
        self.fill_pwdbutton2.grid(row=4, column=1, pady=10)


        self.fill_pwdlabel3 = tk.Label(self.fill_pwdframe, text="El. paštas:")
        self.fill_pwdlabel3.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

        self.fill_pwdentry3 = tk.Entry(self.fill_pwdframe)
        self.fill_pwdentry3.grid(row=6, column=0, padx=10, pady=5)

        self.fill_pwdbutton3 = tk.Button(self.fill_pwdframe, text="Pildyti El. paštą",command=lambda: self.fill(3))
        self.fill_pwdbutton3.grid(row=6, column=1, pady=10)


        self.fill_pwdlabel4 = tk.Label(self.fill_pwdframe, text="Slaptažodis:")
        self.fill_pwdlabel4.grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)

        self.fill_pwdentry4 = tk.Entry(self.fill_pwdframe)
        self.fill_pwdentry4.grid(row=8, column=0, padx=10, pady=5)

        self.fill_pwdbutton4 = tk.Button(self.fill_pwdframe, text="Pildyti slaptažodį",command=lambda: self.fill(4))
        self.fill_pwdbutton4.grid(row=8, column=1, pady=10)

#account management top frame-----------------------------------------------------------------------------------------------------------------------------------
        # Create a frame to contain the UI elements
        self.acc_manager_top_frame = tk.Frame(root)

        # Greyed out section on the left
        self.button0 = tk.Button(self.acc_manager_top_frame, text="Slaptažodžių valdymas", padx=0, pady=0, width=50,command=self.show_password_manager_frame)
        self.button0.grid(row=0, column=0, sticky="new")

        # Button in the middle
        self.button1 = tk.Button(self.acc_manager_top_frame, state='disabled', bg="grey", padx=0, pady=0, width=50)#,command=main_instance.top2_button
        self.button1.grid(row=0, column=1, sticky="new")

        # Button in the right
        self.button2 = tk.Button(self.acc_manager_top_frame, text="Priminimų valdymas", padx=0, pady=0, width=50,command=self.show_reminder_manager_frame)#,command=main_instance.top3_button
        self.button2.grid(row=0, column=2, sticky="new")

        for i in range(3):
            self.acc_manager_top_frame.grid_columnconfigure(i, weight=1)
#---------------------------------------------------
            #acc manager----------------------------------------------------------------------------------------------------------------------------------------------------
        self.account_manager_frame = tk.Frame(root)

        empty_label = tk.Label(self.account_manager_frame, height=3)
        empty_label.grid(row=0, column=0, sticky='ew')

        # Button 1
        self.accmanagerbutton1 = tk.Button(self.account_manager_frame, text="Atsijungti",command=self.logout)
        self.accmanagerbutton1.grid(row=2, column=1, sticky="new")

        # Button 2
        self.accmanagerbutton2 = tk.Button(self.account_manager_frame, text="Redaguoti paskyrą",command=self.show_edit_acc_frame)
        self.accmanagerbutton2.grid(row=4, column=1, sticky="new")

        # Button 3
        self.accmanagerbutton3 = tk.Button(self.account_manager_frame, text="Trinti paskyrą",command=self.delete_account)
        self.accmanagerbutton3.grid(row=6, column=1, sticky="new")

        for i in range(3):
            self.account_manager_frame.grid_columnconfigure(i, weight=1)


        self.acc_manager_top_frame.pack(expand=False, fill=tk.X,anchor="n")
        self.account_manager_frame.pack(expand=True, fill=tk.BOTH,anchor="n")

#REMINDER management top frame-----------------------------------------------------------------------------------------------------------------------------------
        # Create a frame to contain the UI elements
        self.reminder_manager_top_frame = tk.Frame(root)

        # Greyed out section on the left
        self.button0 = tk.Button(self.reminder_manager_top_frame, text="Slaptažodžių valdymas", padx=0, pady=0, width=50,command=self.show_password_manager_frame)
        self.button0.grid(row=0, column=0, sticky="new")

        # Button in the middle
        self.button1 = tk.Button(self.reminder_manager_top_frame, text="Paskyros valdymas", padx=0, pady=0, width=50,command=self.show_account_manager_frame)#,command=main_instance.top2_button
        self.button1.grid(row=0, column=1, sticky="new")

        # Button in the right
        self.button2 = tk.Button(self.reminder_manager_top_frame, state='disabled', bg="grey", padx=0, pady=0, width=50)#,command=main_instance.top3_button
        self.button2.grid(row=0, column=2, sticky="new")
        for i in range(3):
            self.reminder_manager_top_frame.grid_columnconfigure(i, weight=1)
#password management top frame-----------------------------------------------------------------------------------------------------------------------------------
        # Create a frame to contain the UI elements
        self.password_manager_top_frame = tk.Frame(root)

        # Greyed out section on the left
        self.button0 = tk.Button(self.password_manager_top_frame, state='disabled', bg="grey", padx=0, pady=0, width=50)
        self.button0.grid(row=0, column=0, sticky="new")

        # Button in the middle
        self.button1 = tk.Button(self.password_manager_top_frame, text="Paskyros valdymas", padx=0, pady=0, width=50,command=self.show_account_manager_frame)#,command=main_instance.top2_button
        self.button1.grid(row=0, column=1, sticky="new")

        # Button in the right
        self.button2 = tk.Button(self.password_manager_top_frame, text="Priminimų valdymas", padx=0, pady=0, width=50,command=self.show_reminder_manager_frame)#,command=main_instance.top3_button
        self.button2.grid(row=0, column=2, sticky="new")

        for i in range(3):
            self.password_manager_top_frame.grid_columnconfigure(i, weight=1)

        self.password_manager_frame = tk.Frame(root)#PWD MANAGER FRAME--------------------------------------------------------------------------------------------

        empty_label = tk.Label(self.password_manager_frame, height=3)
        empty_label.grid(row=0, column=0, sticky='ew')

        self.pwd_managerbutton1 = tk.Button(self.password_manager_frame, text="Kurti naują", padx=0, pady=0,command=self.show_create_form)#,command=self.something
        self.pwd_managerbutton1.grid(row=2, column=0, sticky="new")



        self.pwd_managerbutton2 = tk.Button(self.password_manager_frame, text="Redaguoti", padx=0, pady=0,command=self.show_edit_form)#,command=self.something
        self.pwd_managerbutton2.grid(row=4, column=0, sticky="new")



        self.pwd_managerbutton3 = tk.Button(self.password_manager_frame, text="Pildyti", padx=0, pady=0,command=self.show_fill_form)#,command=self.something
        self.pwd_managerbutton3.grid(row=6, column=0, sticky="new")


        self.pwd_managerbutton4 = tk.Button(self.password_manager_frame, text="Generuoti slaptažodį", padx=0, pady=0,command=self.show_generate_form)#,command=self.something
        self.pwd_managerbutton4.grid(row=8, column=0, sticky="new")


        self.pwd_managerbutton5 = tk.Button(self.password_manager_frame, text="Trinti", padx=0, pady=0,command=self.delete_record)#,command=self.something
        self.pwd_managerbutton5.grid(row=10, column=0, sticky="new")


        self.updatesearch_var = tk.StringVar()
        self.updatesearch_var.trace("w", lambda name, index, mode: self.update_list())
        self.fillsearch_entry = tk.Entry(self.password_manager_frame, textvariable=self.updatesearch_var)
        self.fillsearch_entry.grid(row=1,columnspan=2,sticky="new")

        self.select_listbox = tk.Listbox(self.password_manager_frame, height=8)
        self.select_listbox.grid(row=2, column=1, sticky="new", rowspan=10)

        #for i in range(12):
        #    self.password_manager_frame.grid_rowconfigure(i, weight=1)


        for i in range(2):
            self.password_manager_frame.grid_columnconfigure(i, weight=1)


        self.edit_acc_frame = tk.Frame(self.root)#EDIT ACC--------------------------------------------------------------------------------------------------------

        self.edit_acc_username_label = tk.Label(self.edit_acc_frame, text="Naujas vartotojo vardas:")
        self.edit_acc_username_entry = tk.Entry(self.edit_acc_frame)

        self.edit_acc_email_label = tk.Label(self.edit_acc_frame, text="Naujas el. paštas:")
        self.edit_acc_email_entry = tk.Entry(self.edit_acc_frame)

        self.edit_acc_password_label = tk.Label(self.edit_acc_frame, text="Naujas slaptažodis:")
        self.edit_acc_password_entry = tk.Entry(self.edit_acc_frame, show="*")

        self.edit_acc_password2_label = tk.Label(self.edit_acc_frame, text="Pakartoti slaptažodį:")
        self.edit_acc_password2_entry = tk.Entry(self.edit_acc_frame, show="*")

        self.edit_acc_button = tk.Button(self.edit_acc_frame, text="Keisti",command=self.edit_acc)#, command=self.edit_acc_user

        # Grid layout for edit_acc form
        self.edit_acc_username_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.edit_acc_username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.edit_acc_email_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.edit_acc_email_entry.grid(row=1, column=1, padx=10, pady=5)

        self.edit_acc_password_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.edit_acc_password_entry.grid(row=2, column=1, padx=10, pady=5)

        self.edit_acc_password2_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.edit_acc_password2_entry.grid(row=3, column=1, padx=10, pady=5)

        self.edit_acc_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.reminder_manager_frame = tk.Frame(root)#REMINDER MANAGER FRAME---------------------------------------------------------------------------------------------------------------------------------

        empty_label = tk.Label(self.reminder_manager_frame, height=3)
        empty_label.grid(row=0, column=0, sticky='ew')

        self.reminder_managerbutton1 = tk.Button(self.reminder_manager_frame, text="Kurti naują", padx=0, pady=0, command=self.show_create_reminder_frame)#,command=self.something
        self.reminder_managerbutton1.grid(row=2, column=0, sticky="new")



        self.reminder_managerbutton2 = tk.Button(self.reminder_manager_frame, text="Redaguoti", padx=0, pady=0,command=self.show_edit_reminder_form)#,command=self.something
        self.reminder_managerbutton2.grid(row=4, column=0, sticky="new")




        self.reminder_managerbutton4 = tk.Button(self.reminder_manager_frame, text="Trinti", padx=0, pady=0,command=self.delete_reminder)#,command=self.something
        self.reminder_managerbutton4.grid(row=6, column=0, sticky="new")


        self.updateremindersearch_var = tk.StringVar()
        self.updateremindersearch_var.trace("w", lambda name, index, mode: self.update_reminder_list())
        self.fillsearch_entry = tk.Entry(self.reminder_manager_frame, textvariable=self.updateremindersearch_var)
        self.fillsearch_entry.grid(row=1,columnspan=2,sticky="new")

        self.reminder_listbox = tk.Listbox(self.reminder_manager_frame, height=5)
        self.reminder_listbox.grid(row=2, column=1, sticky="new", rowspan=5)

        #for i in range(12):
        #    self.reminder_manager_frame.grid_rowconfigure(i, weight=1)


        for i in range(2):
            self.reminder_manager_frame.grid_columnconfigure(i, weight=1)
        


#--------------CREATE REMINDER---------------------------------------------------------------------------------------------------------------------------------
        self.create_reminder_frame = tk.Frame(root)

        self.create_reminder_label1 = tk.Label(self.create_reminder_frame, text="Pavadinimas:")
        self.create_reminder_label1.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.create_reminder_entry1 = tk.Entry(self.create_reminder_frame)
        self.create_reminder_entry1.grid(row=2, column=0, padx=10, pady=5, columnspan=2,sticky="new")


        self.create_reminder_label2 = tk.Label(self.create_reminder_frame, text="Priminimo tekstas:")
        self.create_reminder_label2.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        self.create_reminder_entry2 = tk.Entry(self.create_reminder_frame)
        self.create_reminder_entry2.grid(row=4, column=0, padx=10, pady=5, columnspan=2,sticky="new")


        self.create_reminder_label3 = tk.Label(self.create_reminder_frame, text="Data:")
        self.create_reminder_label3.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

        self.create_reminder_entry3 = DateEntry(self.create_reminder_frame, width=12, background='black',foreground='gray', borderwidth=2, date_pattern='y-mm-dd')
        
        self.create_reminder_entry3.grid(row=6, column=0, padx=10, pady=5, columnspan=2, sticky="new")


        time_options = [f"{hour:02d}:00" for hour in range(0, 24)]

        self.create_reminder_label4 = tk.Label(self.create_reminder_frame, text="Laikas:")
        self.create_reminder_label4.grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)

        self.create_reminder_entry4 = ttk.Combobox(self.create_reminder_frame, values=time_options, state="readonly")
        self.create_reminder_entry4.grid(row=8, column=0, padx=10, pady=5, columnspan=2,sticky="new")
        self.create_reminder_entry4.set(time_options[0])  # Set the default time

        self.create_pwd_button = tk.Button(self.create_reminder_frame, text="Kurti",command=self.create_reminder)
        self.create_pwd_button.grid(row=9, column=0, columnspan=2, pady=10)

        for i in range(2):
            self.create_reminder_frame.grid_columnconfigure(i, weight=1)
#EDIT REMINDER-----------------------------------------------------------------------------------------------------------------------------------
        self.edit_reminder_frame = tk.Frame(root)

        self.edit_reminder_label1 = tk.Label(self.edit_reminder_frame, text="Pavadinimas:")
        self.edit_reminder_label1.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.edit_reminder_entry1 = tk.Entry(self.edit_reminder_frame)
        self.edit_reminder_entry1.grid(row=2, column=0, padx=10, pady=5, columnspan=2,sticky="new")


        self.edit_reminder_label2 = tk.Label(self.edit_reminder_frame, text="Priminimo tekstas:")
        self.edit_reminder_label2.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        self.edit_reminder_entry2 = tk.Entry(self.edit_reminder_frame)
        self.edit_reminder_entry2.grid(row=4, column=0, padx=10, pady=5, columnspan=2,sticky="new")


        self.edit_reminder_label3 = tk.Label(self.edit_reminder_frame, text="Data:")
        self.edit_reminder_label3.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

        self.edit_reminder_entry3 = DateEntry(self.edit_reminder_frame, width=12, background='black',foreground='gray', borderwidth=2, date_pattern='y-mm-dd')
        
        self.edit_reminder_entry3.grid(row=6, column=0, padx=10, pady=5, columnspan=2, sticky="new")


        time_options = [f"{hour:02d}:00" for hour in range(0, 24)]

        self.edit_reminder_label4 = tk.Label(self.edit_reminder_frame, text="Laikas:")
        self.edit_reminder_label4.grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)

        self.edit_reminder_entry4 = ttk.Combobox(self.edit_reminder_frame, values=time_options, state="readonly")
        self.edit_reminder_entry4.grid(row=8, column=0, padx=10, pady=5, columnspan=2,sticky="new")
        self.edit_reminder_entry4.set(time_options[0])  # Set the default time

        self.create_pwd_button = tk.Button(self.edit_reminder_frame, text="Kurti",command=self.edit_reminder)#command=self.edit_reminder
        self.create_pwd_button.grid(row=9, column=0, columnspan=2, pady=10)

        for i in range(2):
            self.edit_reminder_frame.grid_columnconfigure(i, weight=1)

#----

        self.show_register_form()


    def show_create_form(self):
        self.remove_all_frames()
        self.top_frame.pack(expand=False, fill=tk.X,anchor="n")
        self.create_pwd_frame.pack(expand=True, fill=tk.BOTH,anchor="n")
        self.root.title("Kurti naują")

    def show_generate_form(self):
        self.remove_all_frames()
        self.top_frame.pack(expand=False, fill=tk.X,anchor="n")
        self.generate_password_frame.pack(expand=True, fill=tk.BOTH,anchor="n")
        self.generate_password
        self.root.title("Generuoti")





    def show_edit_form(self):
        try:
            index = self.select_listbox.curselection()
            ##print(index )
            #print("\n\n\nDATA: ")
            #print (self.data_manager.data)
            #selected_item = self.data_manager.data[index[0]]
            #print("\n\n\nITEM: ")
            selected_title = self.select_listbox.get(index[0])
            
            # Find the dictionary in the data_manager's data list with the selected title
            selected_item = next((item for item in self.data_manager.data if item['title'] == selected_title), None)
            self.selected_item=selected_item
            #get title from selected item
            
            #self.data_manager.selected_item=item
            self.remove_all_frames()
            self.top_frame.pack(expand=False, fill=tk.X,anchor="n")
            self.edit_pwdframe.pack(expand=True, fill=tk.BOTH,anchor="n")
            #print(selected_item)
            self.root.title("Redaguoti")
            self.edit_pwdentry1.delete(0, tk.END)
            self.edit_pwdentry1.insert(0, selected_item['title'])
            self.edit_pwdentry2.delete(0, tk.END)
            self.edit_pwdentry2.insert(0, selected_item['username'])
            self.edit_pwdentry3.delete(0, tk.END)
            self.edit_pwdentry3.insert(0, selected_item['email'])
            ##print(self.data_manager.saved_key)
            #password2=b'aJ\x1b\xe9\xfa\x94\xaf<~_b\xd2\xca\'\x8c\xeb7\x90\xc1\xdd\xd9\xf6\xac\t\x99\xdbr\x84\xa36vn4\xb4\xe6\x95\t\xc5\xc6\xe2;\x0c"~\xa0U\x00\x002\x88%})\xe4"\x07\xb3\xf6}\x84\xa2\x1f\xb3\xdb\xac\xeb\xbe\xe7\x80:\xb0\x16k<\xe1\x1a;\xa2N\xd9\xb9\xff}\xdb6\x8d\xc0\x94\xf6Z9L\xa6\xe1 \xfay0\xcc\xed\xd73\x933\xd6z\xb3R~x";nq\xa5U\xde\xc2\'\xf0\x18\xd6\xcb\xde\xa8a\xad\xdd\xa7\xebwVi\xc4\xe0\x97\xb5\xa4\xcaf\xbc\\\xe3Y;\xac_m~n\x08T\r\xa1\x9f;J\xee\x0c\x97\xf1\x9c+p\x03u\xe5\x97_/\x163\xeejgs\xdea\xf0@\x9a1\xd0%\x8f\xb9\xa7wr\x97\r\x8ai\x83\x0c\xc8w=4\x16{}\xac\x0c\x0f\xe5Y~\xb6)}B\xf0\xb3\xfd\xbf";Y\x1e\xb6\xceN\x8b\xcb\xc6\xd6\'<\r3\xaf\xc0\xcd\x96q\xe9\x0e\x84\x82Yu\xaa\x12\xd6\xef7+l\xd6\x01\x90\x1d\xafL\xbd'
            password=self.data_manager.decode_base64(selected_item['password'])
            password=self.encryption.decrypt_with_private_key(password,self.data_manager.saved_key)
            #print(password.decode('utf8'))
#           
            self.edit_pwdentry4.delete(0, tk.END)
            self.edit_pwdentry4.insert(0, password.decode('utf8'))

        except IndexError:
            messagebox.showerror("Klaida", "Nepasirinktas įrašas")

    def show_edit_reminder_form(self):
        try:
            index = self.reminder_listbox.curselection()
            #print(index )
            #print("\n\n\nDATA: ")
            #print (self.data_manager.data)
            #selected_item = self.data_manager.data[index[0]]
            #print("\n\n\nITEM: ")
            selected_title = self.reminder_listbox.get(index[0])
            
            # Find the dictionary in the data_manager's data list with the selected title
            selected_item = next((item for item in self.data_manager.reminder_data if item['title'] == selected_title), None)
            self.selected_reminder=selected_item
            #get title from selected item
            
            #self.data_manager.selected_item=item
            self.remove_all_frames()
            self.top_frame.pack(expand=False, fill=tk.X,anchor="n")
            self.edit_reminder_frame.pack(expand=True, fill=tk.BOTH,anchor="n")
            #print(selected_item)
            self.root.title("Redaguoti")
            self.edit_reminder_entry1.delete(0, tk.END)
            self.edit_reminder_entry1.insert(0, selected_item['title'])
            self.edit_reminder_entry2.delete(0, tk.END)
            self.edit_reminder_entry2.insert(0, selected_item['text'])
            #self.edit_reminder_entry3.delete(0, tk.END)
            self.edit_reminder_entry3.set_date(selected_item['date'])
            self.edit_reminder_entry4.delete(0, tk.END)
            self.edit_reminder_entry4.set(selected_item['time'])


        except IndexError:
            messagebox.showerror("Klaida", "Nepasirinktas įrašas")

    def edit_reminder(self):
        title=self.edit_reminder_entry1.get()
        text=self.edit_reminder_entry2.get()
        date=self.edit_reminder_entry3.get()
        time=self.edit_reminder_entry4.get()

        original_title= self.selected_reminder['title']
        creator_id=self.selected_reminder['creator_id']
        response=self.data_manager.edit_reminder(original_title,text,date,time,title,creator_id)
        self.show_reminder_manager_frame()
        if response==False:
            messagebox.showerror("Klaida", "Nepavyko pakeisti")

        pass

    def show_register_form(self):
        self.remove_all_frames()
        self.register_frame.pack(expand=True, fill=tk.BOTH)
        self.root.title("Registracija")

    def show_login_form(self):
        self.remove_all_frames()
        self.login_frame.pack(expand=True, fill=tk.BOTH)
        self.root.title("Prisijungimas")



    #def loading_screen(self):
    #    self.remove_all_frames()
    #    self.loadingframe.pack(expand=True, fill=tk.BOTH)
    #    self.root.title("Registracija")

    def remove_all_frames(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.pack_forget()
                widget.grid_remove()
                for child in widget.winfo_children():
                # If the child is an Entry widget, delete its contents
                    if isinstance(child, tk.Entry):
                        child.delete(0, tk.END)
            widget.pack_forget()
            widget.grid_remove()


    def show_edit_acc_frame(self):
        self.remove_all_frames()
        self.top_frame.pack(expand=False, fill=tk.X,anchor="n")
        self.edit_acc_frame.pack(expand=True, fill=tk.BOTH,anchor="n")
        self.root.title("Redaguoti paskyrą")

        
    def show_password_manager_frame(self):
        self.remove_all_frames()
        self.password_manager_top_frame.pack(expand=False, fill=tk.X,anchor="n")
        self.password_manager_frame.pack(expand=True, fill=tk.BOTH,anchor="n")
        self.update_list()
        self.root.title("Slaptažodžių valdymas")
        self.write_flag = False

    def show_reminder_manager_frame(self):
        self.remove_all_frames()
        self.reminder_manager_top_frame.pack(expand=False, fill=tk.X,anchor="n")
        self.reminder_manager_frame.pack(expand=True, fill=tk.BOTH,anchor="n")
        self.update_reminder_list()
        self.root.title("Priminimų valdymas")
        self.write_flag = False

    def show_account_manager_frame(self):
        self.remove_all_frames()
        self.acc_manager_top_frame.pack(expand=False, fill=tk.X,anchor="n")
        self.account_manager_frame.pack(expand=True, fill=tk.BOTH,anchor="n")
        self.root.title("Paskyros valdymas")
        self.write_flag = False

    def show_create_reminder_frame(self):
        self.remove_all_frames()
        self.top_frame.pack(expand=False, fill=tk.X,anchor="n")
        self.create_reminder_frame.pack(expand=True, fill=tk.BOTH,anchor="n")
        self.root.title("Kurti naują")


    def update_list(self):
        updatesearch_term = self.updatesearch_var.get()
        self.select_listbox.delete(0, tk.END)  # clear the listbox
        for item in self.data_manager.data:
            if updatesearch_term.lower() in item['title'].lower():
                self.select_listbox.insert(tk.END, item['title'])

    def update_reminder_list(self):
        updateremindersearch_term = self.updateremindersearch_var.get()
        self.reminder_listbox.delete(0, tk.END)  # clear the listbox
        for item in self.data_manager.reminder_data:
            if updateremindersearch_term.lower() in item['title'].lower():
                self.reminder_listbox.insert(tk.END, item['title'])

    def login(self):
        try:
            username = self.login_username_entry.get()
            password = self.login_password_entry.get()
            response=self.data_manager.login(username,password)
            ##print(response)
            self.show_password_manager_frame()
        except Exception as e:
            messagebox.showerror("Klaida", "Nepavyko prisijungti")


    def register(self):
                
        username = self.register_username_entry.get()
        email = self.register_email_entry.get()
        password = self.register_password_entry.get()
        password2 = self.register_password2_entry.get()

        if username and password and email:
            if password == password2:
                # Create a directory for each user     


                response=self.data_manager.register(username,email,password)
                if response == False:
                    messagebox.showerror("Klaida", "Nepavyko prisiregistruoti")
                else:
                    self.show_password_manager_frame()
            else:
                messagebox.showerror("Klaida", "Slaptažodžiai nesutampa")
        else:
            messagebox.showerror("Klaida", "Įveskite prisijungimo vardą, el. paštą ir slaptažodį")
        #username = self.login_username_entry.get()
        #password = self.login_password_entry.get()
        #response=self.data_manager.register(username,email,password)
        ##print(response)




    def create(self):
        title = self.create_pwd_entry1.get()
        username = self.create_pwd_entry2.get()
        email = self.create_pwd_entry3.get()
        password = self.create_pwd_entry4.get()
        response=self.data_manager.create(title,username,email,password)


        self.show_password_manager_frame()
        if response == False:
            messagebox.showerror("Klaida", "Nepavyko sukurti")
        pass

    def edit(self):
        title = self.edit_pwdentry1.get()
        username = self.edit_pwdentry2.get()
        email = self.edit_pwdentry3.get()
        password = self.edit_pwdentry4.get()
        original_title= self.selected_item['title']
        response=self.data_manager.edit(title,username,email,password,original_title)
        self.show_password_manager_frame()
        if response==False:
            messagebox.showerror("Klaida", "Nepavyko pakeisti")
    
    def show_fill_form(self):
        try:
            index = self.select_listbox.curselection()
            #print(index )
            #print("\n\n\nDATA: ")
            #print (self.data_manager.data)
            #selected_item = self.data_manager.data[index[0]]
            #print("\n\n\nITEM: ")
            selected_title = self.select_listbox.get(index[0])
            
            # Find the dictionary in the data_manager's data list with the selected title
            selected_item = next((item for item in self.data_manager.data if item['title'] == selected_title), None)
            self.selected_item=selected_item
            #get title from selected item
            
            #self.data_manager.selected_item=item
            self.remove_all_frames()
            self.top_frame.pack(expand=False, fill=tk.X,anchor="n")
            self.fill_pwdframe.pack(expand=True, fill=tk.BOTH,anchor="n")
            #print(selected_item)
            self.root.title("Pildyti formą")
            self.fill_pwdentry1.delete(0, tk.END)
            self.fill_pwdentry1.insert(0, selected_item['title'])
            self.fill_pwdentry2.delete(0, tk.END)
            self.fill_pwdentry2.insert(0, selected_item['username'])
            self.fill_pwdentry3.delete(0, tk.END)
            self.fill_pwdentry3.insert(0, selected_item['email'])
            ##print(self.data_manager.saved_key)
            #password2=b'aJ\x1b\xe9\xfa\x94\xaf<~_b\xd2\xca\'\x8c\xeb7\x90\xc1\xdd\xd9\xf6\xac\t\x99\xdbr\x84\xa36vn4\xb4\xe6\x95\t\xc5\xc6\xe2;\x0c"~\xa0U\x00\x002\x88%})\xe4"\x07\xb3\xf6}\x84\xa2\x1f\xb3\xdb\xac\xeb\xbe\xe7\x80:\xb0\x16k<\xe1\x1a;\xa2N\xd9\xb9\xff}\xdb6\x8d\xc0\x94\xf6Z9L\xa6\xe1 \xfay0\xcc\xed\xd73\x933\xd6z\xb3R~x";nq\xa5U\xde\xc2\'\xf0\x18\xd6\xcb\xde\xa8a\xad\xdd\xa7\xebwVi\xc4\xe0\x97\xb5\xa4\xcaf\xbc\\\xe3Y;\xac_m~n\x08T\r\xa1\x9f;J\xee\x0c\x97\xf1\x9c+p\x03u\xe5\x97_/\x163\xeejgs\xdea\xf0@\x9a1\xd0%\x8f\xb9\xa7wr\x97\r\x8ai\x83\x0c\xc8w=4\x16{}\xac\x0c\x0f\xe5Y~\xb6)}B\xf0\xb3\xfd\xbf";Y\x1e\xb6\xceN\x8b\xcb\xc6\xd6\'<\r3\xaf\xc0\xcd\x96q\xe9\x0e\x84\x82Yu\xaa\x12\xd6\xef7+l\xd6\x01\x90\x1d\xafL\xbd'
            password=self.data_manager.decode_base64(selected_item['password'])
            password=self.encryption.decrypt_with_private_key(password,self.data_manager.saved_key)
            #print(password.decode('utf8'))
#           
            self.fill_pwdentry4.delete(0, tk.END)
            self.fill_pwdentry4.insert(0, password.decode('utf8'))

        except IndexError:
            messagebox.showerror("Klaida", "Nepasirinktas įrašas")


    def fill(self,field):
        #print(field)
        if field ==1:
            data=self.fill_pwdentry1.get()
        elif field==2:
            data=self.fill_pwdentry2.get()
        elif field==3:
            data=self.fill_pwdentry3.get()
        elif field==4:
            data=self.fill_pwdentry4.get()

        pyperclip.copy(data)
        self.write_flag = True

        pass
    def write_text(self):
        #print(self.write_flag)
        if self.write_flag:
            time.sleep(0.25)  # wait for the copy operation to complete
            pyautogui.hotkey('ctrl', 'v')  # paste
            self.write_flag = False

    def on_focus_out(self, event):
        ##print("aaaaaa")
        if event.widget == self.root:
            #print("Root window lost focus")
            self.write_text()


    def delete_record(self):
        index = self.select_listbox.curselection()
        selected_title = self.select_listbox.get(index[0])
        selected_item = next((item for item in self.data_manager.data if item['title'] == selected_title), None)
        self.data_manager.delete_record(selected_item['title'])
        self.show_password_manager_frame()


    def delete_reminder(self):
        try:
            index = self.reminder_listbox.curselection()
            #print(index )
            #print("\n\n\nDATA: ")
            #print (self.data_manager.data)
            #selected_item = self.data_manager.data[index[0]]
            #print("\n\n\nITEM: ")
            selected_title = self.reminder_listbox.get(index[0])
        except IndexError:
            messagebox.showerror("Klaida", "Nepasirinktas įrašas")


    def delete_account(self):
        confirm = messagebox.askokcancel("Patvirtinti", "Ar tikrai norite ištrinti savo paskyrą?")
        
        # If the user confirmed, continue with the method
        if confirm:
            #print("ight")
            self.data_manager.delete_account()
            self.show_register_form()


    def edit_acc(self):

        username = self.edit_acc_username_entry.get()
        email = self.edit_acc_email_entry.get()
        password = self.edit_acc_password_entry.get()
        password2 = self.edit_acc_password2_entry.get()

        if username and password and email:
            if password == password2:
                response=self.data_manager.edit_acc(username,email,password)
                if response== True:
                    self.show_account_manager_frame()
                else:
                    messagebox.showerror("Klaida", "Nepavyko pakeisti duomenų")
            else:
                messagebox.showerror("Klaida", "Slaptažodžiai nesutampa")
        else:
            messagebox.showerror("Klaida", "Įveskite naujus duomenis")

    def create_reminder(self):
        title=self.create_reminder_entry1.get()
        text=self.create_reminder_entry2.get()
        date=self.create_reminder_entry3.get()
        time=self.create_reminder_entry4.get()
        

        response=self.data_manager.create_reminder(title,text,date,time)
        if response==False:
            messagebox.showerror("Klaida", "Nepavyko sukurti")
        else:
            self.show_reminder_manager_frame()

    def delete_reminder(self):
        try:
            index = self.reminder_listbox.curselection()
            selected_title = self.reminder_listbox.get(index[0])
            # Find the dictionary in the data_manager's data list with the selected title
            selected_item = next((item for item in self.data_manager.reminder_data if item['title'] == selected_title), None)
            self.selected_reminder=selected_item

            id=self.selected_reminder['_id']
            self.data_manager.delete_reminder(id)
            self.show_reminder_manager_frame
            self.update_reminder_list
        except IndexError:
            messagebox.showerror("Klaida", "Nepasirinktas įrašas")
        pass

    def generate_password(self):
        # Define the characters that will be used to generate the password
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        punctuation = string.punctuation
        # Ensure each category is represented
        password = [
            secrets.choice(lowercase),
            secrets.choice(uppercase),
            secrets.choice(digits),
            secrets.choice(punctuation)
        ]
        # Generate the rest of the password
        remaining_length = 50 - len(password)
        password += [secrets.choice(lowercase + uppercase + digits + punctuation) for _ in range(remaining_length)]
        # Shuffle to avoid predictable sequences
        secrets.SystemRandom().shuffle(password)
        # Convert list to string and set it as the input for the Entry widget
        self.generate_password_entry1.delete(0, tk.END)
        self.generate_password_entry1.insert(0, ''.join(password))

    def logout(self):

        self.data_manager.saved_key = None
        self.data_manager.public_key = None
        self.data_manager.saved_username = None
        self.data_manager.saved_email = None
        self.data_manager.data=None
        self.data_manager.reminder_data=None
        self.data_manager.selected_item=None
        self.show_login_form()
        pass


root = tk.Tk()
app = Main(root)
#account_manager = AccountManagement(root, DATA_DIR)
#app = AccountManagement(root)
#account_manager.show_register_form()


root.mainloop()