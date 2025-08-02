import tkinter as tk
import json
import random
import time

i=0
start_time = time.time()

data_path = 'data/b1_en_vocab.json'
with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)


random.shuffle(data)


limit = 100

def update_timer():
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    timer_label.config(text=f"Zeit: {minutes:02d}:{seconds:02d}")
    root.after(1000, update_timer)

def mehr():
    global i
    text = data[i]['de']
    num = min(int(1920/len(text)), limit)

    label.config(font=('Helvetica', num))
    label.config(text=text)
    label2.config(text='')
    button.config(text='Offenbaren')
    button.config(command=offenbaren)
    label3.config(text=f"{i}/{len(data)}")

def offenbaren():
    global i
    label2.config(text=data[i]['en'])
    button.config(text='Mehr')
    button.config(command=mehr)
    i += 1

def menu():
    nothing = nothing

def schliessen():
    root.destroy()

def zuruck():
    global i
    i -= 1
    mehr()

root = tk.Tk()
root.geometry('1920x1080')
root.attributes('-fullscreen', True)

label = tk.Label(text='', font=('Arial', 50*3))
label.place(relx=0.5, rely=0.35, anchor='center')

label2 = tk.Label(text='', font=('Arial', 30*3), fg='green')
label2.place(relx=0.5, rely=0.6, anchor='center')

label3 = tk.Label(text=f"{i}/{len(data)}", font=('Arial', 30))
label3.place(relx=0.5, rely=0, anchor='n')

timer_label = tk.Label(text="Zeit: 00:00", font=('Arial', 25))
timer_label.place(relx=0, rely=0, anchor='nw')

   
button = tk.Button(text='Mehr', font=('Arial', 30), command=mehr)
button.place(relx=0.5, rely=0.9, anchor='center')

zuruck_button = tk.Button(text='zurück', font=('Arial', 20), command=zuruck)
zuruck_button.place(relx=0.2, rely=0.9, anchor='center')

schliessen_button = tk.Button(text='EXIT', font=('Arial', 15), command=schliessen)
schliessen_button.place(relx=1, rely=0, anchor='ne')

#menu_button = tk.Button(text='Menu', font=('Arial', 20), command=menu)

# Start the timer
update_timer()

   

root.mainloop()