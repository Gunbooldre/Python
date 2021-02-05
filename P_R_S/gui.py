from tkinter import *
from tkinter.ttk import *
import main


def clicked():
    main.box()
    #secondpage=Tk()\
    lbl.configure(text="P.R.S")
    lbl.grid(column=5, row=0)  
    btnrock = Button(window, image = photoimageofrock, text="Камень",command = main.rock)
    btnpaper = Button(window,image = photoimageofpaper, text="Бумага", command = main.paper)
    btnscis = Button(window,image = photoimageofssc,text="Ножницы",command = main.scissors)
    btnrock.grid(column=3, row=9)
    btnscis.grid(column=5, row=9)
    btnpaper.grid(column=7, row=9)
        
    if main.rock:
        if main.draw:
            win_lose_label.config(text = "You Win")
        elif main.lose:
            win_lose_label.config(text = "Lose")
        if main.win:
            win_lose_label.config(text = "You Win")
    
    
    

            
window = Tk()
window.title("P.R.S")
window.geometry('500x400')
window.iconbitmap('paper.ico')
lbl = Label(window, text="Привет это моя простая игра" , font=("Arial", 25))
lbl.grid(column=5, row=5)
btn = Button(window, text="Старт!", command = clicked)
btn.grid(column=5, row=7)

button_quit = Button(window,text = "Exit", command = window.quit)
button_quit.grid(column = 5, row = 25)

paper_image = PhotoImage(file=r"C:\Users\User\Desktop\P.R.S\pic\paper.gif")
photoimageofpaper = paper_image.subsample(7, 7)

rock_image = PhotoImage(file=r"C:\Users\User\Desktop\P.R.S\roo.gif")
photoimageofrock = rock_image.subsample(6, 6)

ssc_image = PhotoImage(file=r"C:\Users\User\Desktop\P.R.S\pic\scc.gif")
photoimageofssc = ssc_image.subsample(7, 7)

win_lose_label = Label(window,text = "try", font = ("Helvetica",18))
win_lose_label.grid(column = 5, row = 15)



window.mainloop()
