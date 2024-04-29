# cbb_oled_lib.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20
#
##### flash drive ################
# Upload this file to the BlackPill
#
import time
import math
import array

### Definitions ###############
BLACK = 0
WHITE = 1            #On my oled the pixels are blue (yellow in top 2 lines).
OLED_WIDTH = 128
OLED_HEIGHT = 64
BLACK = 0
WHITE = 1
UNFILL = 0
FILLED = 1
ROWHT = 7

### Standalone Functions ###############
# Converted from Kris Kasprzak's c code to MicroPython
# from https://github.com/KrisKasprzak/96_Graphing
#
# drawCircle(myoled, x, y, radius, color, filled)
# drawBarChartV(myoled,curval,loval,hival,inc,dig,label,ReDraw)
# drawBarChartH(d,curval,loval,hival,inc,dig,label,ReDraw)
# drawDial(d,curval,loval,hival,inc,dig,sa,label,ReDraw)

### Class Object and its Functions ###############
# drawList(myoled, title)
#     scale(low,high)
#     clear()
#     show()
#     drawTitle()
#     drawHeader(text)
#     drawScale()
#     drawBarH(val, line)
#     drawData(label, val, line)
#     drawText(self, label, text, line)

def drawCircle(myoled, x, y, radius, color, filled):
    # filled=True or False  color=WHITE=1 or BLACK=0
    myoled.ellipse(x,y,radius,radius,color,filled)
    myoled.show()

def drawBarChartV(myoled,curval,loval,hival,inc,dig,label,ReDraw):
    x=25;y=60;w=40;h=40;
    # inc:increment dig:digits
    if ReDraw == True:
        myoled.fill_rect(0,0, 127,15, WHITE)
        myoled.text(label, 2,4, BLACK)
        stepval = int((inc*h)/(hival - loval) - .001)
        for i in range(0,h,stepval):
            my = y - h + i
            myoled.hline(x+w+1,my, 5, WHITE)
            data = hival - (i * (inc / stepval))
            dat = int(data)
            form = "%.{}f".format(dig)
            text = form % (dat)
            myoled.text(text,x+w+12,my-3, WHITE)
    level = int(h * (((curval - loval) / (hival - loval))))
    myoled.rect(x, y - h, w, h, 1);
    myoled.fill_rect(x, y - h, w, h - level,  BLACK);
    myoled.rect(x, y - h, w, h, 1);
    myoled.fill_rect(x, y - level, w,  level, WHITE);
    myoled.show()
    
def drawBarChartH(d,curval,loval,hival,inc,dig,label,ReDraw):
    x=9;y=45;w=100;h=20;
    if ReDraw == True:
        d.fill_rect(0,0,127,15, WHITE)
        d.text(label, 2,4, BLACK)
        stepval = int((inc*w)/(hival - loval) - .00001)
        for i in range(0,w,stepval):
            d.vline(i+x+2,y,5, WHITE)
            data = (i * (inc/stepval)) + loval + .00001
            dat = int(data)
            form = "%.{}f".format(dig)
            text = form % (dat)
            d.text(text,i+x, y+10, WHITE)
        level = int(w * (((curval - loval) / (hival - loval))))
        d.fill_rect(x + level, y-h, w-level, h,  BLACK)
        d.rect(x, y-h, w,  h, WHITE);
        d.fill_rect(x, y-h, level,  h, WHITE);
        d.show()
        
def drawDial(d,curval,loval,hival,inc,dig,sa,label,ReDraw):
    cx=65;cy=50;r=25;
    degtorad = .0174532778
    if ReDraw == True:
        d.fill_rect(0,0,127,15, WHITE)
        d.text(label, 2,4, BLACK)
        Offset = (270 + sa/2) * degtorad
        stepval = int((inc*sa)/(hival-loval)+ .00)
        #draw dial Characters
        for i in range(0,sa,stepval):
            angle = i*degtorad
            angle = Offset - angle
            ox =  int((r-2) * math.cos(angle) + cx)
            oy =  int((r-2) * math.sin(angle) + cy)
            ix =  int((r-10) * math.cos(angle) + cx)
            iy =  int((r-10) * math.sin(angle) + cy)
            tx =  int((r+10) * math.cos(angle) + cx + 8)
            ty =  int((r+10) * math.sin(angle) + cy)
            d.line(ox, oy, ix, iy, WHITE)
            dat = int(hival - (i * (inc/stepval)))
            form = "%.{}f".format(dig)
            text = form % (dat)
            d.text(text,tx-10,ty,WHITE)
        # draw dial
        for i in range(0, sa):
            angle = i*degtorad
            angle = Offset - angle
            ox =  int((r-2) * math.cos(angle) + cx)
            oy =  int((r-2) * math.sin(angle) + cy)
            d.pixel(ox,oy, WHITE)
        #remove old hand on dial
        d.ellipse(cx,cy,r-8,r-8,BLACK,True)
        # display hand on dial
        angle = sa * (1 - ((curval - loval)/(hival - loval)))
        angle = angle * degtorad
        angle = Offset - angle
        # add new hand on dial
        ix = (r-10)* math.cos(angle)+cx
        iy = (r-10)* math.sin(angle)+cy
        lx = 2*math.cos(angle-90*degtorad)+cx
        ly = 2*math.sin(angle-90*degtorad)+cy
        rx = 2*math.cos(angle+90*degtorad)+cx
        ry = 2*math.sin(angle+90*degtorad)+cy
        ix=int(ix);iy=int(iy);lx=int(lx);ly=int(ly);rx=int(rx);ry=int(ry)
        triangle = array.array('I', [ix,iy,lx,ly,rx,ry])
        d.poly(0,0, triangle, WHITE, True) # Filled
        d.ellipse(cx,cy,3,3,WHITE,True)
        d.show()

class drawList():

    def __init__(self, myoled, title):
        self.oled = myoled
        self.title = title
        self.row = [x for x in range(0,OLED_HEIGHT,8)]
        self.lo = 0
        self.hi = 100
        self.factor = 80
    
    def scale(self,low,high):
        #self.factor = 80 #int((high - low) / (self.hi - self.lo))
        self.lo = low
        self.hi = high
    
    def clear(self):
        self.oled.fill(0)
        self.oled.show()
        
    def show(self):
        self.oled.show()

    def drawTitle(self):
        low = str(self.lo);high = str(self.hi)
        label = low + "-" + high
        pos = 128 - (len(label)*8)
        self.oled.text(self.title, 0, 0, WHITE)
        self.oled.text(label, pos, 0, WHITE)
        #size = 10 - (len(low) + len(high))
    
    def drawHeader(self, text):
        self.oled.text(text, 0, 8, WHITE)
        
    def drawScale(self):
        dot = "."
        for i in range(0,9):
            dot = dot + "."
        #text = str(self.lo) + dot + str(self.hi)
        self.oled.text(dot, 40, 8, WHITE)
        #self.oled.show()

    def drawBarH(self,val, line):
        dat = "{:4.1f}".format(val)
        denom = (self.hi - self.lo)/self.factor
        bar = int((val - self.lo)/denom)
        inc = int((self.hi - self.lo)/10)
        text = ":"+str(inc)
        self.oled.text(text, 0, 8, WHITE)
        #blank last row
        self.oled.fill_rect(0, self.row[line+1], OLED_WIDTH, ROWHT, BLACK)
        self.oled.text(dat, 0, self.row[line+1])
        self.oled.fill_rect(41, self.row[line+1], bar, ROWHT, WHITE)
        for i in range(1,11):
             self.oled.fill_rect(41 + (i * 8), self.row[line+1], 1, ROWHT, BLACK)
        #self.oled.show()
        
    def drawData(self, label, val, line):
        self.oled.fill_rect(0, self.row[line+1], OLED_WIDTH, ROWHT, BLACK)
        text = "{:5.1f}".format(val)
        self.oled.text(label, 0, self.row[line+1])
        self.oled.text(text, 88, self.row[line+1])
        #self.oled.show()
        
    def drawText(self, label, text, line):
        self.oled.fill_rect(0, self.row[line+1], OLED_WIDTH, ROWHT, BLACK)
        self.oled.text(label, 0, self.row[line+1])
        self.oled.text(text, 88, self.row[line+1])
        #self.oled.show()