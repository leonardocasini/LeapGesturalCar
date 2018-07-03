from Tkinter import *
from time import *
import timeit
import tkMessageBox
import urllib2
import cv2
import Tkinter as tk
from PIL import ImageTk, Image

import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = os.path.abspath(os.path.join(src_dir, 'lib'))
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap

from LeapMotionWidget import DriveListener2

class DriveListener(Leap.Listener):
    newBehavior='Try'  
    behavior = 'None'
    #Below attributes is used to chose event gestures
    chooseXDirection=None#3
    chooseYDirection=None#0
    window = None
    #Boolean attributes used to check hand's presence
    defaultLeft = False
    defaultRight = False

    def setFrame(self, caller):
        #It is necessary to call method that chnage appearance of window
        self.window = caller
    
    def on_connect(self, controller):
        print "Connected"

    def on_frame(self, controller):
        boolLeft = False
        boolRight = False
        frame = controller.frame()
        #Initilize boolean false
        self.window.setSwitchColorLeft(False)
        self.window.setSwitchColorRight(False)
        #No Hands
        if len(frame.hands) ==0:
            self.chooseXDirection=0
        #One hand
        elif len(frame.hands) == 1:  
            if frame.hands[0].is_left == False :  
                self.chooseXDirection=0
        
        for hand in frame.hands:
            #handType = "Left hand" if hand.is_left else "Right hand" CI STA DA BUTTARE
            if hand.is_left: 
                boolLeft = True
                #Set direction of car  
                #postive go a head
                if hand.palm_position[2] > 40 : 
                    self.chooseXDirection= 2    
                #negative go back
                elif hand.palm_position[2] < -40 :
                    self.chooseXDirection = 1

            #Normal of hand
            normal = hand.palm_normal

            #Detect right hand
            if not hand.is_left:
                boolRight = True

                #Right hand's roll decide the direction of car
                #Positive 
                if normal.roll* Leap.RAD_TO_DEG  < 30 and normal.roll* Leap.RAD_TO_DEG>-30:
                   self.chooseYDirection=0 
                if normal.roll* Leap.RAD_TO_DEG < -40 :
                   self.chooseYDirection=1
                if normal.roll* Leap.RAD_TO_DEG < -70 :
                    self.chooseYDirection=3
                if  normal.roll* Leap.RAD_TO_DEG > 60 : 
                   self.chooseYDirection=2
                if  normal.roll* Leap.RAD_TO_DEG > 90 :
                    self.chooseYDirection=4
                 
            #Based on the previous checks the attribute newBehavior is set
            if self.chooseXDirection== 0:
                self.newBehavior='halt'
            elif self.chooseXDirection== 1 and self.chooseYDirection==0:
                self.newBehavior='goAhead'
            elif self.chooseXDirection==1 and self.chooseYDirection==1:
                self.newBehavior='DxSoft'
            elif self.chooseXDirection==1 and self.chooseYDirection==3:
                self.newBehavior='DxHard'
            elif self.chooseXDirection==1 and self.chooseYDirection==2:
                self.newBehavior='SxSoft'
            elif self.chooseXDirection==1 and self.chooseYDirection==4:
                self.newBehavior='SxHard'    
            elif self.chooseXDirection==2 and self.chooseYDirection==0:
                self.newBehavior= 'goBack'
            elif self.chooseXDirection==2 and self.chooseYDirection==1:
                self.newBehavior= 'DxSoft2'
            elif self.chooseXDirection==2 and self.chooseYDirection==2:
                self.newBehavior= 'SxSoft2'

            #Below if statement check if there are a changes on bahavior car
            if self.behavior != self.newBehavior:
                #If newBehavior is different from behavior call method and reload attribute behavior 
                self.behavior = self.newBehavior
                if self.behavior == 'DxSoft':
                    self.window.turnDXsoft()
                elif self.behavior == 'goAhead':
                    self.window.GoAhead()
                elif self.behavior == 'SxSoft':
                    self.window.turnSXsoft()
                elif self.behavior == 'SxHard':
                    self.window.turnSXhard()
                elif self.behavior == 'goBack':
                    self.window.goBack()
                elif self.behavior == 'DxHard':
                    self.window.turnDXhard()
                elif self.behavior == 'SxSoft2':
                    self.window.turnDXback()
                elif self.behavior == 'DxSoft2':
                    self.window.turnSXback()
                #Send Http Request with the new behavior                 
                contents = urllib2.urlopen("http://bernice.local/apiLeorio/scriptHalt.php?behavior="+self.behavior).read()

        #if there is a change in hand presence/absent
        if self.defaultLeft != boolLeft:
            #LeftHand founded
            if boolLeft == True:
                self.window.change_color_left_green()
                self.defaultLeft = boolLeft
            #LeftHand not founded
            else:
                self.window.change_color_left_white()
                self.defaultLeft = boolLeft
                #Stop driving car
                contents = urllib2.urlopen("http://bernice.local/apiLeorio/scriptHalt.php?behavior="+'halt').read()            
        if self.defaultRight != boolRight:
            #RightHand founded
            if boolRight == True:
                self.window.change_color2_right_white()
                self.defaultRight = boolRight 
            #RightHand not founded
            else:
                self.window.change_color2_right_white()
                self.defaultRight = boolRight    


class Window:
    def __init__(self):
        #Initialize  a window
        self.window = tk.Tk()
        self.window.configure(background='gray13')
        self.window.protocol('WM_DELETE_WINDOW',self.on_closing)
        self.window.grid()
        self.window.resizable(False,False)

        #Initialize Leap Controller
        self.leap = Leap.Controller()
        
        #Boolen check if start drive
        self.checkStart = False
        
        #Initialize listener and linked to Frame
        self.listener = DriveListener2()#DriveListener()
        self.listener.setFrame(self)
        
        #Two boolean for check state of hands
        self.switchColorLeft = False
        self.switchColorRight = False

        #Set window title and size
        self.window.title( "Control Panel" )
        self.window.geometry( "472x650" )

        #Open image of car go a head
        self.imgGoAhead = Image.open('images/carw.jpg')
        #resize to content of window
        self.imgGoAhead = self.imgGoAhead.resize((461, 507),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(self.imgGoAhead)
        #Set the image on panel
        self.panel = tk.Label(self.window, image = img)
        self.panel.pack(side = "bottom", fill = "both", expand = "yes")
        self.panel.configure(background='black')
        self.panel.grid()
        #Canvas where put two label
        self.canvas = Canvas(self.window, width = 464 ,height = 100, bg = "gray13",highlightbackground= "gray13")
        self.canvas.grid()
        #Two Label initiliza with color white, became green wheen detect hands
        self.textRightHand = self.canvas.create_text(100,50,fill = "white",text='Left hand',font=("Purisa",20))
        self.textLeftHand = self.canvas.create_text(365,50,fill = "white",text='Right hand', font=("Purisa",20))

        #Button connect event start drive
        self.startButton = Button(self.window,text="Start Drive", command= self.startClick,foreground = "red",highlightbackground = "gray13")
        self.startButton.grid()

        #PreCalculate image of rotation car
        self.imgDxSoft = self.imgGoAhead.rotate(-30)
        self.imgSxSoft = self.imgGoAhead.rotate(30)
        self.imgDxHard = self.imgGoAhead.rotate(-60)
        self.imgSxHard = self.imgGoAhead.rotate(60)

        #Open image of car go back with an arrow point down
        self.imgGoBack = Image.open('images/carwback.jpg')
        self.imgGoBack = self.originalGoBack.resize((461, 507),Image.ANTIALIAS)

        #PreCalculate image of rotation car on inversion mode
        self.resizedDxBack = self.resizedGoBack.rotate(-30)
        self.resizedSxBack = self.resizedGoBack.rotate(30)

        self.window.mainloop()
    
    def on_closing(self):
        #if there isn't connection only destroy window else send a comand of halt
        if urllib2.URLError:
            self.window.destroy() 
        else:
            contents = urllib2.urlopen("http://bernice.local/apiLeorio/scriptHalt.php?behavior="+'halt').read() 
            self.leap.remove_listener(self.listener)
            self.window.destroy() 

    #Methods change value of booleans
    def setSwitchColorLeft(self,value):
        self.switchColorLeft=value
    def setSwitchColorRight(self,value):
        self.switchColorRight=value    
    
    #Methods change color of Labels
    def change_color_left_green(self):
        self.canvas.itemconfig(1,fill ="green")
    def change_color_left_white(self):
        self.canvas.itemconfig(1,fill ="white")  
    def change_color_right_green(self):
        self.canvas.itemconfig(2,fill ="green")
    def change_color2_right_white(self):
        self.canvas.itemconfig(2,fill ="white")

    #Events on start drive
    def startClick(self):
        #boolen controll if there some errors
        error = False
        #First click
        if self.checkStart == False:
            self.leap.add_listener(self.listener)
            #check if leap motion device is connected to computer
            if self.leap.is_connected == False:
                tkMessageBox.showerror("Error", 'Connect Leap Motion controller')
                error = True
            else:
                #Try to connect to raspberry sending a commang of halt
                try:
                    contents = urllib2.urlopen("http://bernice.local/apiLeorio/scriptHalt.php?behavior="+'halt').read()
                except urllib2.URLError,e:
                    tkMessageBox.showerror("Error", e.reason)
                    error = True
            
            if error == False:
                self.startButton["text"] = "pause"
                self.checkStart = True
        else:
            self.quitClick()
            #remove listener
            self.leap.remove_listener(self.listener)
            #Change text of button
            self.startButton["text"] = "Restart"
            self.checkStart = False

    #event on close program
    def quitClick(self):
        try:
            contents = urllib2.urlopen("http://bernice.local/apiLeorio/scriptHalt.php?behavior="+'halt').read() 
        except urllib2.URLError,e:
            tkMessageBox.showerror("Error", e.reason)

    #The methods below implements image change
    def turnDXsoft(self):
        img2 = ImageTk.PhotoImage(self.imgDxSoft)
        self.panel.configure(image=img2)
        self.panel.image = img2
    def turnSXsoft(self):
        img2 = ImageTk.PhotoImage(self.imgSxSoft)
        self.panel.configure(image=img2)
        self.panel.image = img2 
    def GoAhead(self):
        img2 = ImageTk.PhotoImage(self.imgGoAhead)
        self.panel.configure(image=img2)
        self.panel.image = img2 
    def goBack(self):
        img2 = ImageTk.PhotoImage(self.imgGoBack)
        self.panel.configure(image=img2)
        self.panel.image = img2
    def turnDXhard(self):
        img2 = ImageTk.PhotoImage(self.imgDxHard)
        self.panel.configure(image=img2)
        self.panel.image = img2
    def turnSXhard(self):
        img2 = ImageTk.PhotoImage(self.imgSxHard)
        self.panel.configure(image=img2)
        self.panel.image = img2
    def turnDXback(self):
        img2 = ImageTk.PhotoImage(self.imgDxBack)
        self.panel.configure(image=img2)
        self.panel.image = img2
    def turnSXback(self):
        img2 = ImageTk.PhotoImage(self.imgSxBack)
        self.panel.configure(image=img2)
        self.panel.image = img2
        

def main():
    Window()

if __name__ == "__main__":
    main()
