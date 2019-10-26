# GUI, this is the driver 

import tkinter as tk
import simulate

root = tk.Tk()
logo = tk.PhotoImage(file="pictures/docbutton.gif")
run = tk.PhotoImage(file="pictures/runButton.gif")
checkIn = tk.PhotoImage(file="pictures/checkInButton.gif")
end = tk.PhotoImage(file="pictures/endButton.gif")
root.configure(background="white")
root.geometry("800x500") #Width x Height
w = tk.Label(root, compound=tk.CENTER,  image=logo).grid(padx=10, row=0, column=0)

runbutton = tk.Button(root, image=run, command=lambda: onclick(1)).grid(padx=10, row=0, column=1)
checkINbutton = tk.Button(root, image=checkIn, command=lambda: onclick(2)).grid(padx=10, row=0, column=2)
endbutton = tk.Button(root, image=end, command=lambda: onclick(3)).grid(padx=10, row=0, column=3)


def onclick(args):
    doctorid = ""
    if args == 1:
        print("yoooo")
    if args == 2:
        doctorid = ""
        label_ci = tk.Label(root, text="Please enter your doctor ID").grid(padx=30, row=1, column=2)
        entry_ci = tk.Entry(root, bd=3).grid(padx=30, row=2, column=2)
        button_ci = tk.Button(root, text="ENTER", command=getdoctor()).grid(row=1, column=3)
    if args == 3:
        exit()
    print(doctorid)

def getdoctor():
    scoreMatrix = [0]
    
    #print(currentScore)
    simulate.simulate(scoreMatrix) ##.score
    
    score = scoreMatrix.pop()
    print("The final score is ", score)

root.mainloop()


