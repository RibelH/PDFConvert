import webbrowser
from tkinter import *
from tkinter import font
from tkinter import filedialog
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import pathlib
root_main = Tk()
root_me = None
root_m = None

image_merge = PhotoImage(file=str(pathlib.Path().absolute()) + "\images\merge.png")
image_merge_encrypt = PhotoImage(file=str(pathlib.Path().absolute()) + "\images\merge_encrypt.png")

#Function for the Main-GUI
def GUI():
    root_main.title("PDF-Merger")
    root_main.geometry("310x200")
    root_main.resizable(False,False)

    m_frame = LabelFrame(root_main)
    m_frame.grid(column =1, row = 2)

    me_frame = LabelFrame(root_main)
    me_frame.grid(column = 2, row = 2)

    Option_text = Label(text="Choose an option:")
    Option_text.grid(column=1, row=1, columnspan=2)
    f_option = font.Font(Option_text, Option_text.cget("font"))
    f_option.configure(weight="bold" )
    Option_text.configure(font=f_option)

    creator = Label(root_main, text= "Created by RibelH",fg="blue")
    f = font.Font(creator, creator.cget("font"))
    f.configure(underline=True)
    creator.configure(font=f)
    creator.bind("<Button-1>", open_github)
    creator.grid(column = 1, row = 3, columnspan = 2)

    b_encrypt = Button(me_frame,command= lambda: GUI_Merge_encrypt()  ,height=150, width=145,image = image_merge_encrypt,
               bg="#378dae", activebackground="#3d9dc2")
    b = Button(m_frame,command = lambda: GUI_Merge(), height =150, width=145, image=image_merge, bg="#378dae", activebackground="#3d9dc2")


    b_encrypt.pack()
    b.pack()

    root_main.mainloop()

# GUI for Merge and Encrypt Function
def GUI_Merge_encrypt():
    global root_me
    global output
    root_me = Toplevel()
    root_me.title("PDF-Merge-Encrypt")
    root_me.geometry("400x275")
    root_me.resizable(False, False)
    #Status update label
    output = Label(root_me, text="", fg="white")
    #Textfield  PDF name
    information_text = Label(root_me, text="Name des zusammengefügten PDFs:")
    information_text.pack(side=TOP)
    name_input = Entry(root_me, bd=5)
    name_input.pack(side =TOP)
    #Text field PDF password
    information_password = Label(root_me, text="Passwort")
    information_password.pack(side=TOP)
    pwd_input =Entry(root_me, bd=5)
    pwd_input.pack(side=TOP)

    me = Button(root_me, command=lambda: merge_encrypt_pdfs(name_input.get() + ".pdf", pwd_input.get()), height=150, width=145,
                image=image_merge_encrypt, bg="#378dae", activebackground="#3d9dc2")
    me.pack(pady=2)

    root_me.mainloop()


# GUI for Merge function
def GUI_Merge():
    global root_m
    global output
    root_m = Toplevel()
    root_m.title("PDF-Merge")
    root_m.geometry("300x230")
    root_m.resizable(False, False)
    #Status update label
    output = Label(root_m, text="", fg="white")
    #Textfield PDF name
    information_text = Label(root_m, text="Name des zusammengefügten PDFs:",)
    information_text.pack(side=TOP)
    name_input = Entry(root_m, bd=5)
    name_input.pack(side=TOP)
    #Merge Button
    m = Button(root_m, command = lambda: merge_pdfs(name_input.get()+".pdf"),height =150, width=145, image=image_merge, bg="#378dae", activebackground="#3d9dc2")
    m.pack(pady=2)

    root_m.mainloop()






#Label das sich updated und den User über den Status des Programms informiert
output = Label(root_main, text="", fg="white")

#Funktion fügt PDF Dokumente zusammen und verschlüsselt diese
def merge_encrypt_pdfs(result_doc, pwd):
    try:
        if pwd =="" and result_doc ==".pdf":
            change_label("Kein Passwort und kein Name eigegeben","red")
            return
        elif result_doc ==".pdf":
            change_label("Keinen Namen eigegeben","red")
            return
        elif pwd == "":
            change_label("Kein Passwort eingegeben","red")
            return

        pdf_writer = PdfFileWriter()

        files = filedialog.askopenfilenames(parent=root_me, title="PDFs auswählen!")

        for file in root_main.tk.splitlist(files):
            pdf_reader = PdfFileReader(file)
            for page in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page))


        if pwd != "":
            change_label("Dokument wird gerade verschlüsselt.....", "black")
            pdf_writer.encrypt(user_pwd=pwd, use_128bit=True)
        with open(result_doc , "wb") as out:
            if pdf_reader.getNumPages() !=0:
                if pwd != "":
                    change_label("Erfolgreich als "+ result_doc + " zusammengefügt und verschlüsselt!", "green")
                else:
                    change_label("Erfolgreich als " + result_doc + " zusammengefügt!", "green")
            else:
                change_label("Keine Dateien ausgewählt.", "red")
            pdf_writer.write(out)

    except:
        change_label("Keine Dateien ausgewählt.", "red")
        os.remove(result_doc)

#Funktion fügt Dokumente zusammen
def merge_pdfs(result_doc):
    try:
        if result_doc ==".pdf":
            change_label("Keinen Namen eigegeben","red")
            return
        pdf_writer = PdfFileWriter()

        files = filedialog.askopenfilenames(parent=root_m, title="PDFs auswählen!")

        for file in root_main.tk.splitlist(files):
            pdf_reader = PdfFileReader(file)
            for page in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page))

        with open(result_doc , "wb") as out:
            if pdf_reader.getNumPages() !=0:

                change_label("Erfolgreich als " + result_doc + " zusammengefügt!", "green")
            else:
                change_label("Keine Dateien ausgewählt.", "red")
            pdf_writer.write(out)

    except:
        change_label("Keine Dateien ausgewählt.", "red")
        os.remove(result_doc)
#Aktualisiert Status des "output" Labels
def change_label(output_text, color):
    output["text"]= output_text
    output["fg"]= color
    output.pack(side=BOTTOM)
#Open GIT-Hub of creator
def open_github(event):
    webbrowser.open("https://github.com/RibelH")


#Start Programm
GUI()