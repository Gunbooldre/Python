# Written by Dias Muratbayev

#Here we import important files
import random
from tkinter import *
from tkinter.ttk import *

#Create a function with name box: we use it for testis
def box():
    box  = ["paper","rock","scissors "]
    print("The game of year")
    print("paper",
      "rock",
      "scissors")
    print("--------------------------------------------------------------")

# Random func
def rando():
    return random.choice(['rock','paper','scissors']) 
#Win func
def win():
    win_lose_label.config(text = "You Win")
#Lose func
def lose():
    win_lose_label.config(text = "Lose")
#draw func
def draw():
    win_lose_label.config(text = "Draw")

#logic for rock
def rock ():
    player = "rock"
    rand = rando()
    if (player == "rock"):
        if(rand == "rock"):
            print("Random choise",rand)
            #print("Draw")
            draw()
        elif (rand == "paper"):
            print("Random choise",rand)
           #print("You Lose")
            lose()
        elif (rand == "scissors"):
            print("Random choise",rand)
          #print("You Win")
            win()
#logic for paper    
def paper():
    player = "paper"
    rand = rando()
    if(player == "paper"):
        if(rand == "rock"):
            print("Random choise",rand)
           # print("You Win")
            win()
        elif (rand == "paper"):
            print("Random choise",rand)
           #print("Draw")
            draw()
        elif (rand == "scissors"):
            print("Random choise",rand)
            #print("You Lose")
            lose()
 #logic for  scissors
def scissors():
    player = "scissors"
    rand = rando()
    if(player == "scissors"):
        if(rand == "rock"):
            print("Random choise",rand)
           # print("You Lose")
            lose()
        elif (rand == "paper"):
            print("Random choise",rand)
           # print("You Win")
            win()
        elif (rand == "scissors"):
            print("Random choise",rand)
           # print("Draw")
            draw()


#Func when we use button "Start"
def clicked():
    box()
    #secondpage=Tk()\
    lbl.configure(text="P.R.S")
    lbl.grid(column=5, row=0)  
    btnrock = Button(window, image = photoimageofrock, text="Камень",command = rock)
    btnpaper = Button(window,image = photoimageofpaper, text="Бумага", command = paper)
    btnscis = Button(window,image = photoimageofssc,text="Ножницы",command = scissors)
    btnrock.grid(column=3, row=9)
    btnscis.grid(column=5, row=9)
    btnpaper.grid(column=7, row=9)
        

#creating our window           
window = Tk()
window.title("P.R.S")
window.geometry('500x400')
window.iconbitmap('paper.ico')
lbl = Label(window, text="Привет это моя простая игра" , font=("Arial", 25))
lbl.grid(column=5, row=5)
btn = Button(window, text="Старт!", command = clicked)
btn.grid(column=5, row=7)

#button to quit from program
button_quit = Button(window,text = "Exit", command = window.quit)
button_quit.grid(column = 5, row = 25)

#We upload pic of paper
paper_image = PhotoImage(file=r"C:\Users\User\Desktop\P.R.S\pic\paper.gif")
photoimageofpaper = paper_image.subsample(7, 7)
#We upload pic of rock
rock_image = PhotoImage(file=r"C:\Users\User\Desktop\P.R.S\roo.gif")
photoimageofrock = rock_image.subsample(6, 6)
#We upload pic of scissors
ssc_image = PhotoImage(file=r"C:\Users\User\Desktop\P.R.S\pic\scc.gif")
photoimageofssc = ssc_image.subsample(7, 7)

#creating "win/lose/draw" lable
win_lose_label = Label(window,text = "try", font = ("Helvetica",18))
win_lose_label.grid(column = 5, row = 15)



window.mainloop()

