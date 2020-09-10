#!/usr/bin/env python
# coding: utf8
# -*- coding: utf-8 -*-

#Este software es de uso personal, no da ninguna garantia
#Podras cifrar tus videos con tecnica de compresion y cifrado Salsa20 y CAST

import tkinter as tk
from tkinter import filedialog,simpledialog,messagebox
import easygui
from PIL import ImageTk, Image
import Crypto 
from Crypto.Cipher import Salsa20,CAST
from Crypto.Hash import SHA256
import pickle
import os
import base64
import zipfile

def label(apli,tex):
    return tk.Label(apli,text=tex)

def entry(apli):
    return tk.Entry(apli)

def button(apli,tex):
    return tk.Button(apli,text=tex)

def comprimir():
    #recogemos la variable global
    global archivo
    global archivoTemp
    #recuperamos el nombre del archivo a comprimir
    filename = os.path.basename(archivo)
    #nombre temporal 
    comprimido = "tempComprimido.zip"
    archivoTemp = comprimido
    #generamos una instancia para almacenar el archivo a comprimir
    jungle_zip = zipfile.ZipFile(comprimido,mode='w')
    #escribimos el archivo
    jungle_zip.write(archivo,filename,compress_type=zipfile.ZIP_DEFLATED)
    #guardamos
    jungle_zip.close()

def borrarComprimido():
    #asi se llamara el archivo temporal
    global archivoTemp
    #borramos el archivo temporal
    os.remove(archivoTemp)

def encode():
    #llamamos a la funcion que comprueba si todo ha ido correctamente
    comprobar()

def estadoBotonDecodificando():
    global app
    boton2Text.set("Codificando...")
    boton2.place(x=32,y=110)
    boton2.config(bg="orange")

def estadoBotonDecodificado():
    boton2Text.set("Codificado")
    boton2.place(x=40,y=110)
    boton2.config(bg="green")
    messagebox.showinfo(title="Codificacion correcta",message="Su archivo ha sido codificado ;)")

def estadoBotonError():
    boton2Text.set("Codificar")
    boton2.place(x=45,y=110)
    boton2.config(bg="blue")
    messagebox.showerror(title="Codificacion Erronea",message="Ocurrio un error al intentar codificar el archivo, el archivo puede estar defectuoso o abierto en el sistema :( ")

def comprobar():
    #recuperamos la instancia de los objetos globales
    global campo, archivo
    #hacemos las validaciones pertinentes
    if(len(campo.get()) < 6):
        messagebox.showwarning(title="El password es demasiado pequeño",message="Por favor, ponga un password de minimo 6 digitos.")
    elif(archivo == ''):
        messagebox.showwarning(title="No hay archivo seleccionado",message="Por favor, seleccione un archivo a codificar.")
    else:
        #cambiamos el estado del boton
        estadoBotonDecodificando()
        #comprimimos el archivo para ahorrar espacio y no perder codificacion original
        comprimir()
        #por ultimo encriptamos
        encriptar(1)
        
def openfile():
  global archivo
  archivo =  tk.filedialog.askopenfilename()
  if(archivo != '' and len(archivo) > 0):
    boton.config(bg="green",fg="white",command=openfile)
  else:
    boton.config(bg="white",fg="black",command=openfile)

def encriptar(version):
    #encriptamos con distintos algoritmos
    global archivoTemp
    global archivo
    global campo
    if(version == 1):
        try:
            secret = encriptarPass(campo.get())
            cipher = Salsa20.new(key=secret)
            cifrado = base64.b64encode(cipher.nonce + cipher.encrypt(open(archivoTemp,'rb').read()))
            guardado = open(encriptarNombre(archivo)+".dat","wb")
            guardado.write(cifrado)
            guardado.close()
            borrarComprimido()
            estadoBotonDecodificado()
        except:
            estadoBotonError()

def encriptarNombre(path):
    global campo
    filename = os.path.basename(path)
    pathname = os.path.dirname(path)
    key = encriptarPassH(campo.get())
    cipher = CAST.new(bytes(key[0:16],"utf-8"), CAST.MODE_OPENPGP)
    newFileName = cipher.encrypt(bytes(filename,"utf-8"))
    return pathname+"/"+str(base64.b64encode(newFileName),'utf-8').replace("/","-@-")

def encriptarPass(valor):
    cipher = SHA256.new(data=bytes(valor,'utf-8'))
    return cipher.digest()

def encriptarPassH(valor):
    cipher = SHA256.new(data=bytes(valor,'utf-8'))
    return cipher.hexdigest()

#variables globales y configuracion inicial (se abre en el centro)
archivo = ''
archivoTemp = ''
app = tk.Tk()
scwidth = app.winfo_screenwidth()
scheight = app.winfo_screenheight()
xcoor = int((scwidth/2) - (290/2))
ycoor = int((scheight/2.4) - (150/2))
app.title("FileEncode KJ v1.Temis")
app.config(bg="black")
app.resizable(False, False)
app.geometry("290x150+{}+{}".format(xcoor, ycoor))
app.iconbitmap(sys._MEIPASS+"\img\encode.ico")

#imagen
image = Image.open(sys._MEIPASS+"\img\code.png")
image = image.resize((100, 150), Image.ANTIALIAS) 
img = ImageTk.PhotoImage(image)
imglabel = tk.Label(app, image=img)    
imglabel.config(bg="black")
imglabel.place(x=80,y=0,relwidth=1, relheight=1)

#titulo version
titulo = label(app,"FileEncode KJ")
titulo.config(justify="left",bg="black",fg="white",font=("Verdana",14))
titulo.pack()
titulo.place(x=0,y=0)

#etiqueta password
etiqueta = label(app,"Password:")
etiqueta.config(justify="left",bg="black",fg="white",font=("Verdana",12))
etiqueta.pack()
etiqueta.place(x=8,y=30)

#campo del password
campo = entry(app)
campo.config(bg="black",fg="white",justify="center",show="*")
campo.pack()
campo.place(x=10,y=52)

#boton para seleccionar archivo
boton = button(app,"Abrir fichero")
boton.config(bg="white",fg="black",command=openfile)
boton.pack()
boton.place(x=35,y=76)

#boton de codificar
boton2 = button(app,"Codificar")
boton2Text = tk.StringVar()
boton2.config(bg="blue",fg="white",textvariable=boton2Text,command=encode)
boton2Text.set("Codificar")
boton2.pack()
boton2.place(x=45,y=110)

#ciclo de vida del entorno grafico
app.mainloop()
