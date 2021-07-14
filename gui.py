from tkinter import *
from tkinter import filedialog
import heapq
import os
import sys
####################huffman



# functions 
def operations(selection):
    operation_type=selection
    input_pass=pathh.get()
     # دة بس اللي محتاج يتعدل و ان نعمل كال للفنكشن. هنا الباس اللي معروف هيطلع علية الاوتبوت
    if (operation_type=='Minifying'):
        pass
        
    elif (operation_type=='prettifying'):
        pass
    elif (operation_type=='xml to json'):
        pass

    elif (operation_type=='visualize errors'):
        pass
    elif (operation_type=='correct errors'):
        pass
    elif (operation_type=='decompress'):
        #input_pass ===.bin
        pass
 
    elif (operation_type=='compress'):
        pass
        




def openFile():
    tf = filedialog.askopenfilename(
        initialdir="C:/Users/MainFrame/Desktop/", 
        title="Open Text file", 
        filetypes=(("Text Files", ".xml .bin"),)
        )
    if tf !="":
        pathh.delete(0, END)
        pathh.insert(0, tf)
        if tf.split(".")[1]=='bin':
            tf = open(tf,"rb")
            file_cont = tf.read()

            txtarea.delete('1.0',"end")
            txtarea.insert('1.0', file_cont)
        
            tf.close()
        else:
            tf = open(tf)
            file_cont = tf.read()

            txtarea.delete('1.0',"end")
            txtarea.insert('1.0', file_cont)
        
            tf.close()



def saveFile():
    tf = filedialog.asksaveasfile(
        mode='w',
        title ="Save file",
        defaultextension=".xml"
        )
    pathh.delete(0,END)
    pathh.insert(0, tf.name)
    data = str(txtarea.get(1.0, END))
    tf.write(data)
   
    tf.close()

ws = Tk()
ws.title("PythonGuides")
ws.geometry("720x500")
ws.resizable(False, False)
ws['bg']='#424242'


# add drop down menu
OPTIONS = [
"Minifying",
"prettifying",
"xml to json",
"visualize errors",
"correct errors",
"compress",
"decompress"
]
variable = StringVar(ws)
variable.set(OPTIONS[0]) # default value
w = OptionMenu(ws, variable, *OPTIONS,command=operations)
w["highlightthickness"]=0
w.pack(pady=5)



# adding frame
frame = Frame(ws)
frame.pack(pady=5)

# adding scrollbars 
ver_sb = Scrollbar(frame, orient=VERTICAL )
ver_sb.pack(side=RIGHT, fill=BOTH)

hor_sb = Scrollbar(frame, orient=HORIZONTAL)
hor_sb.pack(side=BOTTOM, fill=BOTH)

# adding writing space
txtarea = Text(frame,wrap=NONE, width=80, height=20,xscrollcommand=hor_sb.set)
txtarea.pack(side=LEFT)


# binding scrollbar with text area
txtarea.config(yscrollcommand=ver_sb.set)
ver_sb.config(command=txtarea.yview)

txtarea.config(xscrollcommand=hor_sb.set)
hor_sb.config(command=txtarea.xview)


# adding buttons 
openphoto=PhotoImage(file="open.png")
Button(
    ws,activebackground="#424242",bg="#424242",
    image=openphoto,  highlightthickness = 0, bd = 0,
    command=openFile
    ).pack(side=LEFT, padx=5,pady=5)
savephoto=PhotoImage(file="save.png")
Button(
    ws,activebackground="#424242",bg="#424242",
    image=savephoto, highlightthickness = 0, bd = 0,
    command=saveFile
    ).pack(side=LEFT,padx=5,pady=5)
exitphoto=PhotoImage(file="done.png")
Button(
    ws, activebackground="#424242",bg="#424242",
    image=exitphoto, highlightthickness = 0, bd = 0,
    command=lambda:ws.destroy()
    ).pack(side=LEFT, padx=5,pady=5)
"""
Button(
    ws, activebackground="#424242",bg="#424242",
    image=exitphoto, highlightthickness = 0, bd = 0,
    command=lambda:ws.destroy()
    ).pack(side=LEFT, padx=5,pady=5)
"""



pathh = Entry(ws)
pathh.pack(expand=True, fill=X, padx=5)
ws.mainloop()



