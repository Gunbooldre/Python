import random
import sys
import os
##import pygame
from tkinter import *
#from datetime import datetime
#now = datetime.now()

#song = pyglet.media.load('TheFatRat – Unity.mp3')
#song.play()
#pyglet.app.run()


class Game:
    def __init__(self):
        self.window= Tk() 
        self.window.title("Hangman")
        self.canvas=Canvas(window, width=600, height= 600)
        self.canvas.pack()
        self.tutorial="""Hello,my friends,let's play!!!
        hangman is a paper and pencil guessing game for two or more players.
        one player thinks of a word, phrase or sentence and the other tries
        to guess it by suggesting letters within a certain number of guesses"""
        self.canvas.create_text(320,50,text=tutorial,fill="black",font=("Times new roman ","14"))

        self.btn_Countries=Button(window,text="Countries",width=30,height=3,command=lambda: slova () )

        self.btn_lessons=Button(window,text="Lessons",width=30,height=3,command=lambda:slova() )

        self.btn_animals=Button(window,text="Animals",width=30,height=3,command=lambda:slova() )

        self.btn_common=Button(window,text="Common",width=30,height=3,command=lambda:slova() )

        self.btn_animals.place(x=200,y=310)

        self.btn_common.place(x=200,y=370)

        self.btn_lessons.place(x=200,y=490)

        self.btn_animals["bg"]="green"

        self.btn_lessons["bg"]="darkcyan"

        self.btn_common["bg"]="red"

        self.btn_Countries.place(x=200,y=430)

        self.btn_Countries["bg"]="Firebrick"

        self.window.mainloop()
        pass
    def fon (self):
        y=0
        while y < 600:
            x = 0
            while x < 600:
                self.canvas.create_rectangle(x, y , x+33 , y+43, fill = "white" , outline = "blue")
                x=x+33
            y=y+43
    def DeleteButtons(self):
        self.btn_Countries.destroy()
        self.btn_animals.destroy()
        self.btn_common.destroy()
        self.btn_lessons.destroy()

    def slova(self):
        self.DeleteButtons()
        self.fon()
        self.file=open("words.txt")
        self.key=[line.strip() for line in file]
        self.word=random.choice(key)
        self.wo=word[1:-1]
        self.wor=[]
    for i in wo:
        wor.append(i)
        self.a0=canvas.create_text (282,40,text=word[0],fill="black",font=("Times new roman ","18"))
        self.a1=canvas.create_text(315,40,text="_",fill="black",font=("Times new roman ","18"))
        self.a2=canvas.create_text(347,40,text="_",fill="black",font=("Times new roman ","18"))
        self.a3=canvas.create_text(380,40,text="_",fill="black",font=("Times new roman ","18"))
        self.a4=canvas.create_text(412,40,text="_",fill="black",font=("Times new roman ","18"))
        self.a5=canvas.create_text(444,40,text="_",fill="black",font=("Times new roman ","18"))
        self.a6=canvas.create_text(477,40,text="_",fill="black",font=("Times new roman ","18"))
        self.a7=canvas.create_text(510,40,text=word[-1],fill="black",font=("Times new roman ","18"))
        pass
    pass


    
    lis1=[1,2,3,4,5,6]
    alphabet="qwertyuiopasdfghjklzxcvbnm"
    err=[]
    win=[]

    def igra (b):
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
                canvas.create_text(150,150,text="You win", fill="black",font=("Times new roman ","18"))
                btn_again = Button(window, text="Again", width=30, height=3, command=lambda:slova() )
                for i in alphabet:
                    btn[i]["state"]="disabled"
        else:
            err.append(b)
            btn[k]["bg"]="red"
            btn[k]["state"]="disabled"
            #if len (err)==1:
            #    #golovo
            #elif len (err)==2:
            #    #telo
            #elif len (err)==3:
            #    #lefthand
            #elif len(err)==4:
            #    #rigth g=hand
            #elif len(err)==5:
            #    #left leg
            #elif len(err)==6:
            #    #rigth hand 
                #end()
    btn={}
    def gen (u,x,y):
        btn[u]=Button  (window,text=u,width=3,height=1,command=lambda: igra(u))
        btn[u].place(x=str(x),y=str(y))
    x=265
    y=110
    for i in alphabet[0:8]:
        gen(i,x,y)
        x=x+33
    x=265
    y=137
    for i in alphabet[8:16]:
        gen(i,x,y)
        x=x+33
    x=265
    y=164
    for i in alphabet[16:24]:
        gen(i,x,y)
        x=x+33
    x=265
    y=191
    for i in alphabet[24:26]:
        gen(i,x,y)
        x=x+33
def end ():
    canvas.create_text (150,150,tetx="You lose", fill="red",font=("Times new roman ","18"))
    for i in alphabet:
        btn[i]["state"]="disable"