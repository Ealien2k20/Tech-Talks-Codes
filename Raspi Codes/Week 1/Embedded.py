#########################################################Importing Essential Libraires
import RPi.GPIO as GPIO                                 #For controlling GPIO(General Purpose Input Output) pins of Raspbery pi 
                                                        #
GPIO.setwarnings(False)                                 #If the previous programs were not closed properly, the GPIO pins will still
                                                        #be running and this line ignores the warning due to such issues
                                                        #
GPIO.setmode(GPIO.BOARD)                                #There are two modes, GPIO.BOARD and GPIO.BCM The numbering of the pins are ordered in GPIO.BOARD
                                                        #hence, we prefer that setting. See the image PIN.jpg
                                                        #
GPIO.setup(11,GPIO.IN)                                  #PIN 11 will act as input pin to obtain input form PIR sensor.
GPIO.setup(12,GPIO.OUT)                                 #PIN 12 will act as output pin to control the servo motor.
p=GPIO.PWM(12,50)                                       #PIN 12 will act as a PWM pin to provide square pulses of variable width to control the servo motor.
                                                        #The frequency of the square pulses is 50 Hz, i.e, the time period of the square pulses will be 20 milliseconds
p.start(6)                                              #Turn on the PWM pulses in pin 12 with a duty cycle of 6%(It will be one for 6% of the time period and off for 94% of the time period)
                                                        #i.e, ON time:1.2 milliseconds  OFF time:18.8 milliseconds
#########################################################                                            
#The Servo motor is controlled by 20 millisecond pulses #
#of various ON times.ON time of 1 millisecond=0 degree  #
#and ON time of 1.5 millisecond=90 degree               #
#ON time of 2 millisecond=180 degree. Most Servo motors #
#rotate only till 180 degree.                           #                                                                                        
#########################################################
while True:                                             #Infinite Loop (Most of the real time applications consist of an infinite loop)
    x=GPIO.input(11)                                    #Obtain the Input from PIR Sensor
    print(x)                                            #Print the sensor value in the screen
    if x==1:                                            #If a human is present x will be 1,hence turn the servo motor to 180 degrees position(Duty cycle of 10%)
        p.ChangeDutyCycle(10)                           #
    else:                                               #
        p.ChangeDutyCycle(7.5)                          #If a human is not present x will be 0,hence turn the servo motor to 90 degrees position
                                                        #
#########################################################
