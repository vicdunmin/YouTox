#!/usr/bin/env python3

import tkinter as tk
from tkinter import *
from PIL import Image

class Bar:
    def __init__(self,x0,y0,x1,y1):
        self.x0 = x0; self.y0 = y0
        self.x1 = x1; self.y1 = y1
    def draw(self,canvas,fill):
        canvas.create_rectangle(self.x0,self.y0,self.x1,self.y1,fill=fill)

class SearchBar(Bar):
    def __init__(self,x0,y0,x1,y1):
        super().__init__(x0,y0,x1,y1)

    def draw(self,canvas,fill,width,height,typing,query):
        super().draw(canvas,fill)
        size = self.y1-self.y0
        searchX0 = 3*(self.x0+self.x1)//4
        self.searchX0 = searchX0
        canvas.create_rectangle(searchX0,self.y0,
                                self.x1,self.y1,fill="gold",outline=None)
        canvas.create_text((searchX0+self.x1)//2,(self.y0+self.y1)//2,
                            text="Search",fill="darkBlue")
        margin = 5
        if typing:
            canvas.create_text((self.x0+self.searchX0)//2,
                                (self.y0+self.y1)//2,text=str(query),
                                anchor="center",
                                font="Helvetica "+str(int(size*0.25))+" bold")

    def inSearchBar(self,x,y):
        return self.x0<=x<=self.searchX0 and self.y0<=y<=self.y1

class NavigationBar(Bar):
    items = ["Home","About","Youtube"]
    def __init__(self,x0,y0,x1,y1):
        super().__init__(x0,y0,x1,y1)
    def draw(self,canvas,fill):
        super().draw(canvas,fill)
        self.width = (self.x0+self.x1)*0.2
        self.height = self.y1-self.y0
        for i in range(4):
            centerY = self.height//2
            centerX = (i*self.width+(i+1)*self.width)/2
            if i < 3:
                canvas.create_rectangle(i*self.width,0,
                                        (i+1)*self.width,
                                        self.height,fill=fill)
                canvas.create_text(centerX,centerY,text=NavigationBar.items[i])
            else:
                centerX = (i*self.width+(i+2)*self.width)/2
                canvas.create_text(centerX,centerY,text="YouTox",fill="black",
                                font = "Helvetica "+str(int(self.height//2))+" bold")
    def inWhichItem(self,x,y):
        for i in range(3):
            if i*self.width<=x<=(i+1)*self.width and 0<=y<=self.height:
                return NavigationBar.items[i]

class Logo:
    def __init__(self):
        pass

def init(d):
    d.mode = "HomePage"; d.modes = ["HomePage","AboutPage","YoutubePage"]
    d.queries = ["",""]; d.maxLength = 50
    d.typingHome = False
    d.typingYoutube = False
    d.description = """YouTox is an application that labels and\nsummarizes toxicity and polarity of comments"""
    d.query = "Enter a URL to analyze comment toxicity"
    d.about = "YouTox is tkinter application that employs logistic regression\nand" + \
              "sentiment analysis to determine polarity of comments"

def drawStartPage(c,d):
    logo = PhotoImage(file='logo.gif')
    logo = logo.subsample(2,2)
    label = Label(image=logo)
    label.image = logo # keep a reference!
    label.place(x=100,y=100)
    n = NavigationBar(0,0,d.width,50)
    d.navigationBar = n
    n.draw(c,"lightblue")
    margin = 10
    s = SearchBar(margin,d.height*0.5,d.width-margin,d.height*0.6)
    d.startSearch = s
    s.draw(c,None,d.width,d.height,d.typingHome,d.queries[0])
    c.create_text(d.width//2,d.height//3,text=d.description,
                  font="Helvetica "+str(int(d.height*0.035))+" bold")
    # label.pack()

    #c.create_image(100,100,image = logo)


def drawAboutPage(c,d):
    n = NavigationBar(0,0,d.width,50)
    d.navigationBar = n
    n.draw(c,"lightblue")
    margin = 10
    c.create_text(d.width//2,d.height//3,text=d.about,
                  font="Helvetica "+str(int(d.height*0.035))+" bold")
                  
def drawYoutubePage(c,d):
    n = NavigationBar(0,0,d.width,50)
    n.draw(c,"lightblue")
    margin = 10
    s = SearchBar(margin,d.height*0.5,d.width-margin,d.height*0.6)
    d.youtubeSearch = s
    s.draw(c,None,d.width,d.height,d.typingYoutube,d.queries[0])
    c.create_text(d.width//2,d.height//3,text=d.query,
                  font="Helvetica "+str(int(d.height*0.035))+" bold")

def drawDataPage(c,d):
    pass

def timerFired(d):
    pass

def editQuery(e,d,i,typing):
    if typing and len(d.queries[0]) < d.maxLength:
        if e.keysym == "BackSpace":
            d.queries[0] = d.queries[0][:-1]
        elif e.keysym == "Return":
            pass
        else:
            d.queries[0] += e.char
    else:
        if e.keysym == "BackSpace":
            d.queries[0] = d.queries[0][:-1]

def keyPressed(e,d):
    if d.mode == "HomePage":
        editQuery(e,d,0,d.typingHome)
    if d.mode == "YoutubePage":
        editQuery(e,d,1,d.typingYoutube)

def changePage(e,d):
    for i in range(len(d.modes)):
        item = d.navigationBar.inWhichItem(e.x,e.y)
        if item != None and item in d.modes[i]:
            d.mode = d.modes[i]; d.queries = ["",""]
            d.typingHome = False; d.typingYoutube = False

def mousePressed(e,d):
    if d.mode == "HomePage":
        if d.startSearch.inSearchBar(e.x,e.y):
            d.typingHome = True
        changePage(e,d)
    elif d.mode == "YoutubePage":
        print(d.youtubeSearch.inSearchBar(e.x,e.y))
        if d.youtubeSearch.inSearchBar(e.x,e.y):
            d.typingYoutube = True
        changePage(e,d)
    elif d.mode == "AboutPage":
        changePage(e,d)

def redrawAll(c,d):
    if d.mode == "HomePage":
        drawStartPage(c,d)
    elif d.mode == "AboutPage":
        drawAboutPage(c,d)
    elif d.mode == "YoutubePage":
        drawYoutubePage(c,d)
    elif d.mode == "DataPage":
        drawDataPage(c,d)
    

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed

if __name__ == "__main__":
    run(700, 700)


