from tkinter import *
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox
import sys

root = Tk()
root.title('FUT Stat Traker')

#creating and connecting to the database
conn = sqlite3.connect('fut_stat.db')
c = conn.cursor()
#create the table for the database
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
#function for when the submit button is pressed
def submit():
    #handle some errors so the user does not enter invalid data
    try:
        int(iuserscore.get())
        int(opponetscore.get())
        if pen.get() == 1:
            int(penuserscore.get())
            int(penoppscore.get())
        elif pen.get() == 0:
            if penuserscore.get() or penoppscore.get():
                messagebox.showinfo("WARNING", "INVALID ENTRY")
                int(penuserscore.get())
                int(penoppscore.get())
                return
            
            
    except:
        messagebox.showinfo("WARNING","INVALID ENTRY")
        return
    
    conn = sqlite3.connect('fut_stat.db')
    c = conn.cursor()
    #get all the data from user and enter it to the database
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
    #clear the data after the user submit it
    iuserscore.delete(0,END)
    opponetscore.delete(0,END)
    clickedresult.set("Win")
    clicked.set("WL")
    etv.set(0)
    pen.set(0)
    penuserscore.delete(0,END)
    penoppscore.delete(0,END)
    gameend.set("Normal")
#function for when the show button is press it show everything in the database
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
#function to delete the last entry on the database
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
#function to popup the grpah the user wants
def graph1(self):
    conn = sqlite3.connect('fut_stat.db')
    c = conn.cursor()

    c.execute("SELECT *, oid FROM gamestats")
    entries = c.fetchall()
    
    scoregraph = []
    scoregraphopp = []
    modedata = []
    extratimedata = []
    penplayed = []
    penscore = []
    penscoreopp = []
    hiedata = []
    resultdata = []
    #getting all the data from the database and seperating it 
    p =''
    for x in entries:
        info = str(x).replace(')','').replace('(','').replace('u\'','').replace("'","")
        infosplit = info.split(',')
        scoreappend = infosplit[0] 
        scoreappendopp = infosplit[1]
        modeappend = infosplit[2]
        etappend = infosplit[3]
        penplayeddata = infosplit[4]
        penscoreappend = infosplit[5].replace(' ','')
        penscoreoppappend = infosplit[6].replace(' ','')
        wltappend = infosplit[7]
        wolappend = infosplit[8]


        scoregraph.append(scoreappend)
        scoregraphopp.append(scoreappendopp)
        modedata.append(modeappend)
        extratimedata.append(etappend)
        penplayed.append(penplayeddata)
        penscore.append(penscoreappend)
        penscoreopp.append(penscoreoppappend)
        hiedata.append(wltappend)
        resultdata.append(wolappend)
    
        
        penscore = list(filter(("").__ne__,penscore))
        penscoreopp = list(filter(("").__ne__,penscoreopp))
        
    #get the user choice 
    o = graphseleted.get()
    #displays a bar graphs for ech the users goals score in each game and also the opponents
    if o == "Goals":
        plt.close()
        newg = [int(i) for i in scoregraph]
        newop = [int(j) for j in scoregraphopp]
        f, (ax1, ax2) = plt.subplots(1,2)
        labels, counts = np.unique(newg,return_counts=True)
        labels2, counts2 = np.unique(newop,return_counts=True)
        ax1.bar(labels,counts,align='center')
        ax2.bar(labels2,counts2,align='center')
        plt.gca().set_xticks(labels)
        ax1.set(xlabel='Goals Score',ylabel='# of games')  
        ax2.set(xlabel='Goals Score',ylabel='# of games')
        ax1.set_title("My Goals")
        ax2.set_title("Opponents Goals")
        plt.show()
    #displays a pie graph with the % of each mode the user played
    elif o == "% Mode Played":
        plt.close()
        wl = 0
        r = 0
        for a in modedata:
            if a == " WL":
                wl = wl + 1
            elif a == " Rivals":
                r = r + 1
        labels = 'WL', 'Rivals'
        arr = np.array([wl,r])
        plt.pie(arr,labels=labels, autopct='%1.1f%%')
        plt.show()
    #display a pie graph with the % of the WIN LOSE AND TIE
    elif o == "W/L/T Ratio":
        plt.close()
        w = 0
        l = 0
        t = 0
        for a in resultdata:
            if a == " Win":
                w = w + 1
            elif a == " Lose":
                l = l + 1
            elif a == " Tie":
                t = t + 1
        labels = 'WIN', 'LOSE', 'TIE'
        arr = np.array([w,l,t])
        plt.pie(arr,labels=labels, autopct='%1.1f%%')
        plt.show()
    #display same as goals but for pens
    elif o == "Pens":
        plt.close()
        newpen = [int(i) for i in penscore]
        newpenopp = [int(j) for j in penscoreopp]
        f, (ax1, ax2) = plt.subplots(1,2)
        labels, counts = np.unique(newpen,return_counts=True)
        labels2, counts2 = np.unique(newpenopp,return_counts=True)
        ax1.bar(labels,counts,align='center')
        ax2.bar(labels2,counts2,align='center')
        plt.gca().set_xticks(labels)
        ax1.set(xlabel='Pens Score',ylabel='# of games')  
        ax2.set(xlabel='Pens Score',ylabel='# of games')
        ax1.set_title("My Pens Goals")
        ax2.set_title("Opponents Pens Goals")
        plt.show()
    #diplay the % of how the game ended 
    elif o == "How it Ended":
        plt.close()
        n = 0
        rq = 0
        dc = 0
        for a in hiedata:
            if a == " Normal":
                n = n + 1
            elif a == " Rage Quit":
                rq = rq + 1
            elif a == " DC":
                dc = dc + 1 
        labels = 'Normal', 'Rage Quit', 'Tie'
        arr = np.array([n,rq,dc])
        plt.pie(arr,labels=labels, autopct='%1.1f%%')
        plt.show() 
    
    conn.commit()
    conn.close()
    
#create all the labels, entries, buttons, checkboxs, and dropdown menus 
titlescore = Label(root, text="Score: ")
titlescore.grid(row=1, column=0)
ct = Label(root, text = " : ").grid(row=1, column=2)
iuserscore = Entry(root,width=2)
iuserscore.grid(row=1, column=1)
opponetscore = Entry(root,width=2)
opponetscore.grid(row=1, column=3)

resultl = Label(root,text="Result: ").grid(row=3,column=0)
clickedresult = StringVar()
clickedresult.set("Win")
resultm = OptionMenu(root, clickedresult, "Win", "Lose", "Tie")
resultm.grid(row=3,column=1)

clicked = StringVar()
clicked.set("WL")
gamemode = Label(root,text="Mode: ").grid(row=3,column=2)
gameselection = OptionMenu(root, clicked, "WL", "Rivals")
gameselection.grid(row=3,column=3)

etv = IntVar()
et = Checkbutton(root, text="Extra Time",variable=etv)
et.grid(row=2,column=4,sticky=W)

pen = IntVar()
penc = Checkbutton(root, text="Penaties", variable=pen)
penc.grid(row=2,column=0)


penuserscore = Entry(root, width = 2)
penuserscore.grid(row=2,column=1)
ctt = Label(root,text=" : ")
ctt.grid(row=2,column=2)
penoppscore = Entry(root, width = 2)
penoppscore.grid(row=2, column=3)

gameend = StringVar()
gameend.set("Normal")
ge = Label(root,text="How it ended: ")
ge.grid(row=1, column=4)
ges = OptionMenu(root, gameend, "Normal", "Rage Quit", "DC")
ges.grid(row=1, column=5)

submitbtn = Button(root,text="Submit", command=submit)
submitbtn.grid(row=3,column=4,columnspan=2)

showbtn = Button(root,text="Show",command=show)
showbtn.grid(row=3,column=6,sticky=W)

delete_lastrecourd = Button(root,text="Delete Last Entry",command=delete)
delete_lastrecourd.grid(row=1,column=6)

graphseleted = StringVar()
graphseleted.set("Select Data to Graph")
grhsel=OptionMenu(root, graphseleted, "Goals", "% Mode Played", "W/L/T Ratio","Pens","How it Ended",command=graph1)
grhsel.grid(row=2,column=5,columnspan=2,sticky=W)

conn.commit()

conn.close()


root.mainloop()
