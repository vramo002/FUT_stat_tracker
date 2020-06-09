from tkinter import *
import sqlite3
import numpy as np
import matplotlib.pyplot as plt


root = Tk()
root.title('FUT Stat Traker')

conn = sqlite3.connect('fut_stat.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS gamestats (
         userscore integer,
         oppscore integer,
         mode text,
         extra_time integer,
         penalties integer,
         puscore integer,
         poscore integer,
         hie text,
         result text
         )""")

def submit():
    conn = sqlite3.connect('fut_stat.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO gamestats VALUES (:A,:B,:C,:D,:E,:F,:G,:H,:I)",
            {
                'A':iuserscore.get(),
                'B':opponetscore.get(),
                'C':clicked.get(),
                'D':etv.get(),
                'E':pen.get(),
                'F':penuserscore.get(),
                'G':penoppscore.get(),
                'H':gameend.get(),
                'I':clickedresult.get()
            })    

    conn.commit()
    conn.close()
    #clear
    iuserscore.delete(0,END)
    opponetscore.delete(0,END)
    clickedresult.set("Win")
    clicked.set("WL")
    etv.set(0)
    pen.set(0)
    penuserscore.delete(0,END)
    penoppscore.delete(0,END)
    gameend.set("Normal")

def show():
    conn = sqlite3.connect('fut_stat.db')
    c = conn.cursor()
    
    c.execute("SELECT *, oid FROM gamestats")
    records = c.fetchall()

    print_records=''
    for i in records:
        print_records += str(i) + "\n"

    l = Label(root,text=print_records)
    l.grid(row=5,column=0,columnspan=7)

    conn.commit()
    conn.close()

def delete():
    conn = sqlite3.connect('fut_stat.db')
    c = conn.cursor()

    c.execute("SELECT *, oid FROM gamestats")
    items = c.fetchall()
    num = 0
    for value in items:
        num = num + 1
    
    c.execute("DELETE from gamestats WHERE oid= " + str(num))
    
    conn.commit()
    conn.close()

def graph1(self):
    conn = sqlite3.connect('fut_stat.db')
    c = conn.cursor()

    c.execute("SELECT userscore FROM gamestats")
    entries = c.fetchall()
    
    p =''
    for x in entries:
        p += str(x) 
    print(type(p))
    
    o = graphseleted.get()
    if o == "Goal":
        plt.hist(p)
        plt.show()

    conn.commit()
    conn.close()
    

title = Label(root, text="Fut Stat Traker")
title.grid(row=0, column=0,columnspan=4)

titlescore = Label(root, text="Score: ")
titlescore.grid(row=1, column=0)
ct = Label(root, text = " : ").grid(row=1, column=2)
iuserscore = Entry(root,width=2)
iuserscore.grid(row=1, column=1)
opponetscore = Entry(root,width=2)
opponetscore.grid(row=1, column=3)

resultl = Label(root,text="Result: ").grid(row=1,column=4)
clickedresult = StringVar()
clickedresult.set("Win")
resultm = OptionMenu(root, clickedresult, "Win", "Lose", "Tie")
resultm.grid(row=1,column=5)

clicked = StringVar()
clicked.set("WL")
gamemode = Label(root,text="Mode: ").grid(row=1,column=6)
gameselection = OptionMenu(root, clicked, "WL", "Rivals")
gameselection.grid(row=1,column=7)

etv = IntVar()
et = Checkbutton(root, text="Extra Time",variable=etv)
et.grid(row=2,column=0)

pen = IntVar()
penc = Checkbutton(root, text="Penaties", variable=pen)
penc.grid(row=2,column=1)


penuserscore = Entry(root, width = 2)
penuserscore.grid(row=2,column=2)
ctt = Label(root,text=" : ")
ctt.grid(row=2,column=3)
penoppscore = Entry(root, width = 2)
penoppscore.grid(row=2, column=4)

gameend = StringVar()
gameend.set("Normal")
ge = Label(root,text="How it ended: ")
ge.grid(row=2, column=5)
ges = OptionMenu(root, gameend, "Normal", "Rage Quit", "DC")
ges.grid(row=2, column=6)

submitbtn = Button(root,text="Submit", command=submit)
submitbtn.grid(row=3,column=0,columnspan=7)

showbtn = Button(root,text="Show",command=show)
showbtn.grid(row=4,column=0)

delete_lastrecourd = Button(root,text="Delete Last Entry",command=delete)
delete_lastrecourd.grid(row=4,column=1)

graphseleted = StringVar()
graphseleted.set("Select Data to Graph")
grhsel=OptionMenu(root, graphseleted, "Goal", "Record", "WL",command=graph1)
grhsel.grid(row=5,column=0)

conn.commit()

conn.close()


root.mainloop()