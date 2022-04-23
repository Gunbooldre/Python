from tkinter import *

start = True
lastcommand = "="
result = 0
def click(text):
    global start
    global lastcommand
    global display
    if text.isdigit() or text == '.':
        if start:
            display.configure(text='')
            start = False
        if text != '.' or display.cget('text').find('.') == -1:
            display.configure(text=(display.cget('text') + text))
    else:
        if start:
            lastcommand = text
        else:
            calculate(float(display.cget('text')))
            lastcommand = texts
            start = True
            
def calculate(x):
    global lastcommand
    global result
    global display
    if lastcommand == '+':
        result += x
    elif lastcommand == '-':
        result -= x
    elif lastcommand == '*':
        result *= x
    elif lastcommand == '/':
        try:
            result /= x
        except ZeroDivisionError:
            pass
    elif lastcommand == '=':
        result = x
    display.configure(text=result)
    
window = Tk()

window.title("Calculator")

buttons = (('7','8','9','/'),
          ('4','5','6','*'),
          ('1','2','3','-'),
          ('0','.','=','+'))

display= Label(window,text = "0", font = "Tahoma 20",bd = 10)
display.grid(row = 0, column = 0, columnspan  = 4)
for row in range(4):
    for column in range(4):
        button = Button(window,text = buttons[row][column],font = "Tahoma 20", command = lambda text =buttons[row][column]:click(text))
        button.grid(row=row+1,column=column+1,padx=5, pady = 5, ipadx = 20, ipady = 20, sticky = 'nsew')
        button.bind
w = window.winfo_reqwidth()
h = window.winfo_reqheight()

ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()

x = int(ws/2 - w/2)
y = int(hs/2 - h/2)

window.geometry("+{0}+{1}".format(x,y))

window.mainloop()