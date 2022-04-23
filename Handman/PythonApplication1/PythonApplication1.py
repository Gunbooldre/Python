import random
import os
import pygame
from tkinter import *
from PIL import ImageTk, Image
import pyglet
pyglet.lib.load_library('avbin')
pyglet.have_avbin=True
#from datetime import datetime
#now = datetime.now()
window= Tk() 
window.title("Hangman")
canvas=Canvas(window, width=600, height=600)
canvas.pack()


song = pyglet.media.load('thefatrat – unity.mp3')
song.play()
btn={}

alphabet="qwertyuiopasdfghjklzxcvbnm"
def fon ():
    img = ImageTk.PhotoImage(Image.open("fon.jpg"))
    canvas.create_image(220, 220, image=img)
    canvas.image = img
    p.palka()
    p.palka2()
    pass

tutorial="""Hello,my friends,let's play!!!
hangman is a paper and pencil guessing game for two or more players.
one player thinks of a word, phrase or sentence and the other tries
to guess it by suggesting letters within a certain number of guesses"""
canvas.create_text(320,50,text=tutorial,fill="black",font=("Times new roman ","14"))

def DeleteButtons():
    btn_Countries.destroy()
    btn_animals.destroy()
    btn_common.destroy()
    btn_lessons.destroy()
    pass

def CreateButtons():
    globals()['btn_Countries']=Button(window,text="Countries",width=30,height=3,command=lambda: slova('Countries') )

    globals()['btn_lessons']=Button(window,text="Lessons",width=30,height=3,command=lambda:slova('lessons') )

    globals()['btn_animals']=Button(window,text="Animals",width=30,height=3,command=lambda:slova('animals') )

    globals()['btn_common']=Button(window,text="Common",width=30,height=3,command=lambda:slova('common') )

btn_Countries=Button(window,text="Countries",width=30,height=3,command=lambda: slova('Countries') )

btn_lessons=Button(window,text="Lessons",width=30,height=3,command=lambda:slova('lessons') )

btn_animals=Button(window,text="Animals",width=30,height=3,command=lambda:slova('animals') )

btn_common=Button(window,text="Common",width=30,height=3,command=lambda:slova('common') )

fl=['animals',"common","lessons","Countries"]
def start():
    CreateButtons()


    btn_animals.place(x=200,y=310)

    btn_common.place(x=200,y=370)

    btn_lessons.place(x=200,y=490)

    btn_animals["bg"]="green"

    btn_lessons["bg"]="darkcyan"

    btn_common["bg"]="red"

    btn_Countries.place(x=200,y=430)

    btn_Countries["bg"]="Firebrick"

def slova(fileName):
    global btn
    DeleteButtons()
    fon()
    file = open('{0}.txt'.format(fileName), 'r')

    key=[line.strip() for line in file]
    word=random.choice(key)
    wo=word[1:-1]
    wor=[]
    for i in wo:
        wor.append(i)
    try:
        a0=canvas.create_text (282,40,text=word[0],fill="black",font=("Times new roman ","18"))
    except:
        print(word)
    print(key)
    a1=canvas.create_text(315,40,text="_",fill="black",font=("Times new roman ","18"))
    a2=canvas.create_text(347,40,text="_",fill="black",font=("Times new roman ","18"))
    a3=canvas.create_text(380,40,text="_",fill="black",font=("Times new roman ","18"))
    a4=canvas.create_text(412,40,text="_",fill="black",font=("Times new roman ","18"))
    a5=canvas.create_text(444,40,text="_",fill="black",font=("Times new roman ","18"))
    a6=canvas.create_text(477,40,text="_",fill="black",font=("Times new roman ","18"))
    a7=canvas.create_text(510,40,text=word[-1],fill="black",font=("Times new roman ","18"))
    
    lis1=[1,2,3,4,5,6]
    err=[]
    win=[]

    def igra (b):
        global alphabet
        ind_alf=alphabet.index(b)
        k=alphabet[ind_alf]

        if b in wor:

            ind=wor.index(b)
            b2=lis1[ind]
            wor[ind]='1'
            
            def kord():
                if b2 == 1:
                    x1,y1=315,40
                if b2 == 2:
                    x1,y1=347,40
                if b2 == 3:
                    x1,y1=380,40
                if b2 == 4:
                    x1,y1=412,40
                if b2 == 5:
                    x1,y1=444,40
                if b2 == 6:
                    x1,y1=477,40
                return x1,y1
            x1,y1=kord()

            win.append(b)
            a  =canvas.create_text(x1,y1,text=wo[ind],fill="black",font=("Times new roman ","18"))
            btn[k]["bg"]="green"

            if not b  in wor:
                btn[k]["state"]="disabled"
            if b in wor :
                win.append(b)
                ind1=wor.index(b)
                b2=lis1[ind1]
                x1,y1=kord()
                canvas.create_text(x1,y1,text=wo[ind1],fill="black",font=("Times new roman ","18"))
            if len (win) == 6:
                canvas.create_text(500,350,text="You win", fill="lime",font=("Times new roman ","18"))
                start()

                btn_again = Button(window, text="Again", width=30,height=3,command=lambda:start() )
                btn_again.place(x=200,y=490)
                btn_again["bg"]="red"

                for i in alphabet:
                    btn[i]["state"]="disabled"
        else:
            err.append(b)
            btn[k]["bg"]="red"
            btn[k]["state"]="disabled"

            if len (err)==1:
                h.golova()
            elif len (err)==2:
                h.telo()
            elif len (err)==3:
                h.lefthand()
            elif len(err)==4:
                h.rigthhand()
            elif len(err)==5:
                h.leftleg()
            elif len(err)==6:
                h.rigthleg()
                end(fileName)
            window.update()
    
    def gen (u,x,y):
        global btn
        btn[u]=Button  (window,text=u,width=5,height=2,command=lambda: igra(u))
        btn[u].place(x=str(x),y=str(y))
    x=265
    y=110
    for i in alphabet[0:8]:
        gen(i,x,y)
        x=x+33
    x=265
    y=147
    for i in alphabet[8:16]:
        gen(i,x,y)
        x=x+33
    x=265
    y=184
    for i in alphabet[16:24]:
        gen(i,x,y)
        x=x+33
    x=265
    y=220
    for i in alphabet[24:26]:
        gen(i,x,y)
        x=x+33

class Hangman:
    def golova(self):
        canvas.create_oval(90,50,120,80,width=4,fill="white")
        window.update()
    def telo(self):
        canvas.create_line(100,80,100,200,width=4)
        window.update()
    def lefthand(self):
        canvas.create_line(100,80,145,100,width=4)
        window.update()
    def rigthhand(self):
        canvas.create_line(100,80,45,100,width=4)
        window.update()
    def leftleg(self):
        canvas.create_line(100,200,45,280,width=4)
        window.update()
    def rigthleg(self):
        canvas.create_line(100,200,145,280,width=4)
        window.update()

h = Hangman()
class palka:
    def palka(self):
        canvas.create_line(25,580,20,35,width=4)
    def palka2(self):
        canvas.create_line(25,38,120,40,width=4)
p=palka()




def end (fileName):
    global btn
    canvas.create_text (350,350,text="You lose", fill="red",font=("Times new roman ","18"))

    for i in alphabet:
        btn[i]["state"]="disable"
    btn_again = Button(window, text="Again", width=30,height=3,command=start )
    btn_again.place(x=200,y=490)
    btn_again["bg"]="red"



start()
window.mainloop()