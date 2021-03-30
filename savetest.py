# -*- coding: utf-8 -*-
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageGrab
#import Tkinter as tk
#import tkFileDialog
#import tkMessageBox
#from tkFileDialog import askopenfilename
#from Tkinter import Button, Entry, Label
#import tkFileDialog as fd
#import tkSimpleDialog
#import tkMessageBox as messagebox
#import tkSimpleDialog as simpledialog

import tkinter as tk
from tkinter import filedialog as fd
from tkinter import Button, Entry, Label,messagebox, simpledialog

im= None
tk_img= None
tk_update = None






# 파일메뉴에서“열기”를선택하였을때호출되는함수
def open():
    global im, tk_img
    fname= fd.askopenfilename()
    im= Image.open(fname)
    #비율계산하기
    x=im.width
    y=im.height
    a=x/y
    roundwidth=round(480*a)
    roundheight=round(720/a)
    if a<=1.5:
        im=im.resize((int(roundwidth), 480),Image.ANTIALIAS)
    else:
        im=im.resize((720, int(roundheight)),Image.ANTIALIAS)
    
    tk_img= ImageTk.PhotoImage(im)
    
    canvas.create_image(360 , 240, image=tk_img)
    
    window.update()
    
# 파일메뉴에서“종료”를선택하였을때호출되는함수
def quit():
    if messagebox.askokcancel("Quit", "종료하시겠습니까?"):
        window.destroy()

def save():
    global im, tk_img
    toSave = fd.asksaveasfile(mode='w',defaultextension='.jpg')
    tk_img.save(toSave)

    	
def image_rotate():
    global im, tk_img

    im = im.rotate(45)
    tk_img= ImageTk.PhotoImage(im)
    canvas.create_image(360 , 240, image=tk_img)
    window.update()

    
# 영상처리메뉴에서“열기”를선택하였을때호출되는함수
def image_blur():
    global im, tk_img
    out = im.filter(ImageFilter.BLUR)
    tk_img= ImageTk.PhotoImage(out)
    canvas.create_image(360 , 240, image=tk_img)
    window.update()
    
def process1():#샤프하게
    global im, tk_img
    out = im.filter(ImageFilter.UnsharpMask(radius=2, percent=150,threshold=3))
    tk_img= ImageTk.PhotoImage(out)
    canvas.create_image(360 , 240, image=tk_img)
    window.update()

def process2():#살짝 은은한
    global im, tk_img
    out = im.filter(ImageFilter.MedianFilter(size=3))
    tk_img= ImageTk.PhotoImage(out)
    canvas.create_image(360 , 240, image=tk_img)
    window.update()

def process3():#대조
    global im, tk_img
    cont=simpledialog.askstring('Contrast','Enter the values(0~1):',parent=window)
    
    if float(cont)>1 or float(cont)<0:
        messagebox.showinfo("Error", "values must be between 0 to 1")
        window.update()
    else:
        enhancer=ImageEnhance.Contrast(im)
        out=enhancer.enhance(float(cont))
        tk_img= ImageTk.PhotoImage(out)
        canvas.create_image(360, 240, image=tk_img)
        window.update()
    

def process4():#밝기
    global im, tk_img
    brit=simpledialog.askstring('Brightness','Enter the values(0~1):',parent=window)
    enhancer=ImageEnhance.Brightness(im)
    if float(brit)>1 or float(brit)<0:
        messagebox.showinfo("Error", "values must be between 0 to 1")
        window.update()
    else:
        out=enhancer.enhance(float(brit))
        tk_img= ImageTk.PhotoImage(out)
        canvas.create_image(360, 240, image=tk_img)
        window.update()

def process5():#원래대로
    global im, tk_img
    tk_img=ImageTk.PhotoImage(im)
    canvas.create_image(360 , 240, image=tk_img)
    window.update

def getter():
    x=window.winfo_rootx()+canvas.winfo_x()
    y=window.winfo_rooty()+canvas.winfo_y()
    x1=x+canvas.winfo_width()
    y1=y+canvas.winfo_height()
    toSave = fd.asksaveasfile(mode='w',defaultextension='.jpg')
    ImageGrab.grab().crop((x+40,y,x1-45,y1-75)).save(toSave)
    
window=tk.Tk() #window
canvas = tk.Canvas(window, width = 720, height = 550, bg='slategrey')
canvas.pack()



menubar= tk.Menu(window)
filemenu= tk.Menu(menubar)
ipmenu= tk.Menu(menubar)
filemenu.add_command(label="열기", command=open)
filemenu.add_command(label="종료", command=quit)
filemenu.add_command(label="저장", command=lambda:getter())
menubar.add_cascade(label="파일", menu=filemenu)
window.config(menu=menubar)


l1=Label(window, bg='grey',highlightcolor='black')
l1.place(width=730, height= 80, x=0,y=480)

name=['Rotate', 'Blur', 'Unsharp\nMask','median\nfilter','Contrast','Brightness']
commands=[image_rotate, image_blur, process1, process2, process3, process4]
bgcolors=[]

for i in range(6):
    b=Button(window,text=name[i], command=commands[i], bg='black', fg='white', activebackground='skyblue',relief='groove')
    b.place(width= 60, height = 50, x=90+(60*i), y=490)


Clearbt = Button(window,text='origin',command=process5)
Clearbt.pack()
Clearbt.place(width=50,height=50,x=680,y=0)

window.mainloop() #창띄우기


