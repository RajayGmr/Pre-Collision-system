import RPi.GPIO as GPIO
import time
import keyboard
GPIO.setmode(GPIO.BCM)

#Motor PIN NO
in1 = 23
in2 = 24
in3 = 22
in4 = 27
enA = 25
enB = 17
temp1=1


GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)

GPIO.setup(enA,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

p=GPIO.PWM(enA,1000)
p1=GPIO.PWM(enB,1000)
p1.start(25)
p.start(25)

def stop():
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.LOW)
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.LOW)

def forward():
	GPIO.output(in1,GPIO.HIGH)
	GPIO.output(in2,GPIO.LOW)
	GPIO.output(in3,GPIO.HIGH)
	GPIO.output(in4,GPIO.LOW)
	temp1=1
	
    
def backward():
	 GPIO.output(in1,GPIO.LOW)
	 GPIO.output(in2,GPIO.HIGH)
	 GPIO.output(in3,GPIO.LOW)
	 GPIO.output(in4,GPIO.HIGH)
	 temp1=0
	 
    
def goright():
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.LOW)
	GPIO.output(in3,GPIO.HIGH)
	GPIO.output(in4,GPIO.LOW)
	
	

def goleft():
	GPIO.output(in1,GPIO.HIGH)
	GPIO.output(in2,GPIO.LOW)
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.LOW)
	

def distanceMeasurement(TRIG,ECHO):

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulseStart = time.time()
    while GPIO.input(ECHO) == 1:
        pulseEnd = time.time()

    pulseDuration = pulseEnd - pulseStart
    distance = pulseDuration * 17150
    distance = round(distance, 4)
    return distance

#Configuration
#Backside
GPIO.setup(7,GPIO.OUT) #Trigger
GPIO.setup(8,GPIO.IN)  #Echo
#Right
GPIO.setup(9,GPIO.OUT) #Trigger
GPIO.setup(10,GPIO.IN)  #Echo
#Middle
GPIO.setup(19,GPIO.OUT) #Trigger
GPIO.setup(26,GPIO.IN)  #Echo
#Left
GPIO.setup(20,GPIO.OUT) #Trigger
GPIO.setup(21,GPIO.IN)  #Echo


#Security
GPIO.output(7, False)
GPIO.output(9, False)
GPIO.output(19, False)
GPIO.output(20, False)
time.sleep(0.5)

#main Loop
try:
    while True:
       for i in range(4):
           if i == 0:
               recoveredDistanceBK = distanceMeasurement(7,8)
               print "Distance from The Backside: ",recoveredDistanceBK,"cm"
           elif i == 1:
               recoveredDistanceR = distanceMeasurement(9,10)
               print "Distance from The Right: ",recoveredDistanceR,"cm"
           elif i == 2:
               recoveredDistanceM = distanceMeasurement(19,26)
               print "Distance from The Middle: ",recoveredDistanceM,"cm"
           elif i == 3:
               recoveredDistanceL = distanceMeasurement(20,21)
               print "Distance from The Left: ",recoveredDistanceL,"cm"
       time.sleep(0.5)	

       
       if (recoveredDistanceM>40 and recoveredDistanceL>10 and recoveredDistanceR>10):
		   print "The machine goes forward. \n"
		   forward()
		   time.sleep(.6)
		   stop()		
       elif (recoveredDistanceM>40 and recoveredDistanceL<40 and recoveredDistanceR>40)or(recoveredDistanceM<40 and recoveredDistanceL<40 and recoveredDistanceR>40):
		   print "The machine goes right. \n"
		   goleft()
		   time.sleep(.6)
		   stop()
       elif (recoveredDistanceM>40 and recoveredDistanceL>40 and recoveredDistanceR<40)or(recoveredDistanceM<40 and recoveredDistanceL>40 and recoveredDistanceR<40):
		   print "The machine goes left. \n"
		   goright()
		   time.sleep(.6)
		   stop()
       elif (recoveredDistanceM<40):
		   print "The machine goes backward. \n"
		   backward()
		   time.sleep(.6)
		   stop()		  			
       else:
		   print "The machine goes right. \n"
		   goleft()
		   time.sleep(.6)
		   stop()							
except KeyboardInterrupt:
    print "The System has TERMINATED"
    stop()
