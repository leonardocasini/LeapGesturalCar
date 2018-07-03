import os, sys
import time
import RPi.GPIO as GPIO
# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)

# set up the GPIO channels
r1 = 16 #DX Anteriore
r2 = 26 #DX Posteriore
r3 = 21 #SX Anteriore
r4 = 20 #SX Posteriore
r5 = 12 #DX Anteriore 2
r6 = 19 #Dx Posteriore 2
r7 = 13 #SX Anteriore 2
r8 = 6 #SX Posteriore 2
GPIO.setup(r1, GPIO.OUT) # GPIO 0
GPIO.setup(r2, GPIO.OUT) # GPIO 1
GPIO.setup(r3, GPIO.OUT) # GPIO 2
GPIO.setup(r4, GPIO.OUT) # GPIO 3
GPIO.setup(r5, GPIO.OUT) # GPIO 4
GPIO.setup(r6, GPIO.OUT) # GPIO 5
GPIO.setup(r7, GPIO.OUT) # GPIO 6
GPIO.setup(r8, GPIO.OUT) # GPIO 7


def halt():
	GPIO.output(r1, True) #GPI O a 1 Led acceso
	GPIO.output(r2, True) #GPI 1 a 1 Led acceso
	GPIO.output(r3, True) #GPI 2 a 1 Led acceso
	GPIO.output(r4, True) #GPI 3 a 1 Led acceso
	GPIO.output(r5, False) #GPI 4 a 1 Led acceso
	GPIO.output(r6, False) #GPI 5 a 1 Led acceso
	GPIO.output(r7, False) #GPI 6 a 1 Led acceso
	GPIO.output(r8, False) #GPI 7 a 1 Led acceso

#Pin setting for each wheels
def DxAnt():
	GPIO.output(r3, True)
	GPIO.output(r7, True)
def DxPost():
	GPIO.output(r1, True)
	GPIO.output(r5, True)
def SxAnt():
	GPIO.output(r4, True)
	GPIO.output(r8, True)
def SxPost():
	GPIO.output(r2, True)
	GPIO.output(r6, True)
def DxAnt2():
	GPIO.output(r4, False)
def DxPost2():
	GPIO.output(r3, False)
def SxAnt2():
	GPIO.output(r2, False)
def SxPost2():
	GPIO.output(r1, False)


#Once the pins have been set, we made the turning methods 
def goAhead():
	halt()
	DxAnt()
	SxAnt()
	DxPost()
	SxPost()

def goBack():
	halt()
	DxAnt2()
	SxAnt2()
	DxPost2()
	SxPost2()

def DxSoft():
	halt()
	SxAnt()
	DxPost()
	SxPost()

def DxHard():
	halt()
	SxAnt()
	SxPost()

def SxSoft():
	halt()
	DxAnt()
	DxPost()
	SxPost()

def SxHard():
	halt()
	DxAnt()
	DxPost()

def SxSoft2():
	halt()
	SxAnt2()
	DxPost2()
	DxAnt2()

def SxHard2():
	halt()
	DxAnt2()
	DxPost2()

def DxSoft2():
	halt()
	DxAnt2()
	SxPost2()
	SxAnt2()

def DxHard2():
	halt()
	DxAnt2()
	DxPost2()


if __name__ == '__main__':


	if len(sys.argv) > 1:
		behavior = str(sys.argv[1])
	#Behavior set on LeapMotionWidget decide which pins active
	if behavior == "halt":
		halt()
	elif behavior == "goAhead":
		goAhead()
	elif behavior == "goBack":
		goBack()
	elif behavior == "SxSoft":
		SxSoft()
	elif behavior == "SxHard":
		SxHard()
	elif behavior == "DxSoft":
		DxSoft()
	elif behavior == "DxHard":
		DxHard()
	elif behavior == "SxSoft2":
		SxSoft2()
	elif behavior == "SxHard2":
		SxHard2()
	elif behavior == "DxSoft2":
		DxSoft2()
	elif behavior == "DxHard2":
		DxHard2()
	
	elif behavior == "test":
		#Some command to check if working
		halt()
		SxAnt()
		time.sleep(1)
		halt()
		SxPost()
		time.sleep(1)
		halt()
		DxPost()
		time.sleep(1)
		halt()
		DxAnt()
		time.sleep(1)
		halt()
	


	
