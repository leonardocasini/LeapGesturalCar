import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = os.path.abspath(os.path.join(src_dir, 'lib'))
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap

class DriveListener2(Leap.Listener):
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

