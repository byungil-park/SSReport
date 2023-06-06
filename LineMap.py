from tkinter import *
from tkinter.font import *
from PIL import Image, ImageTk

scale = 0
x, y = 0, 0
s = None
img = None
olde = None

def InitMap(frame):
    global s, img
    s = Image.open('LineMap.png')
    #s.show()
    #s_size = s.size
    #print(s_size)
    s1 = s.resize((600, 600))
    #s1_size = s1.size
    #print(s1_size)
    Smap = ImageTk.PhotoImage(s1)
    img = Label(frame, width=600-15,height=600-15, bg='white')
    img.image = Smap
    img.configure(image=Smap)
    img.place(x=0,y=0)

    img.bind_all('<Up>', move)
    img.bind_all('<Down>', move)
    img.bind_all('<Left>', move)
    img.bind_all('<Right>', move)
    img.bind('<B1-Motion>',Mousemove)

    buttonfont = Font(family='맑은 고딕', size=12, weight='bold')

    Button(frame, text=' + ', font=buttonfont, command=sizeDown).pack(side=RIGHT, anchor='s')
    Button(frame, text=' - ', font=buttonfont, command=sizeUp).pack(side=RIGHT, anchor='s')

def UpdateMap():
    global img
    s1 = s.resize((590+scale*240, 600+scale*185))
    s1 = s1.crop((x,y,x+600,y+600))
    Smap = ImageTk.PhotoImage(s1)
    img.image = Smap
    img.configure(image = Smap)
    #print(scale, x, y)

def sizeDown():
    global scale
    scale = min(scale + 1, 7)
    UpdateMap()

def sizeUp():
    global scale
    scale = max(scale - 1, 0)
    UpdateMap()

def move(e):
    global x, y
    if e.keysym == 'Down':
        y = min(y+20, scale*190)
    elif e.keysym == 'Up' and y > 0:
        y -= 20
    elif e.keysym == 'Right':
        x = min(x+20, scale*230)
    elif e.keysym == 'Left' and x > 0:
        x -= 20
    UpdateMap()

def Mousemove(e):
    global x,y,olde

    if olde != None:
        dx, dy = e.x - olde.x, e.y - olde.y
        if abs(dx) + abs(dy) > 100:
            dx, dy = 0,0
        x = max(0, min(x-dx, scale*230))
        y = max(0,min(y-dy, scale*190))
        print(dx, dy)
    olde = e
    UpdateMap()

'''root = Tk()
root.geometry('600x600')
InitMap(root)
root.mainloop()'''