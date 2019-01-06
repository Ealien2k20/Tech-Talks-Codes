
#NOTE:
#Before looking at this code visit embeddey.py of Week 1 to know more about the servo motor.


#################################################################Import
import time                                                     #For manual delays in operations.
import RPi.GPIO as GPIO                                         #For controlling the GPIO(General Purpose Input Output) pins of Raspberry pi.
import socket                                                   #For Communicating with other devices on the internet

GPIO.setwarnings(False)                                         #If the previous programs were not closed properly, the GPIO pins will still
                                                                #be running and this line ignores the warning due to such issues

GPIO.setmode(GPIO.BOARD)                                        #There are two modes, GPIO.BOARD and GPIO.BCM The numbering of the pins are ordered in GPIO.BOARD
                                                                #hence, we prefer that setting. See the image PIN.jpg in week1

GPIO.setup(12,GPIO.OUT)                                         #PIN 12 will act as output pin to control the servo motor.
p=GPIO.PWM(12,50)                                               #PIN 12 will act as a PWM pin to provide square pulses of variable width to control the servo motor.
                                                                #The frequency of the square pulses is 50 Hz, i.e, the time period of the square pulses will be 20 milliseconds
p.start(6)                                                      #Turn on the PWM pulses in pin 12 with a duty cycle of 6%(It will be one for 6% of the time period and off for 94% of the time period)
                                                                #i.e, ON time:1.2 milliseconds  OFF time:18.8 milliseconds

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)           #To work with sockets to communicate on the internet we need to create socket objects which
                                                                #Have the essential function to work with to do networking operations
                                                                #Like sending and recieveing data
sock.bind(("192.168.1.103",4000))                               #Associate our socket with the IP adress of raspi and make port 4000 open for communication with other devices
print("Waiting for connection")                                 #Waits for other devices to connect if socket was created without error
                                                                #Make sure you give the correct IP address which can be found in Raspberry pi's task bar
sock.listen(5)                                                  #Upto 5 devices can connect to Raspberry pi
conn,ip=sock.accept()                                           #Conn is the socket which is created when an external device establishes connection with raspberry pi
                                                                #ip is the ip address of that device
print("Connected to "+str(ip[0])+" on port "+str(ip[1]))        #Prints the details
while True:                                                     #Infinite loop
        size=40                                                 #The size of the string which we will be recieving is 40 characters 
        door=""                                                 #The string door will hold the recieved string.
        while(not (size==0)):                                   #This loop makes sure that we receive all the 40 characters and waits till that happens.
            door+=conn.recv(40)                                 #Append the newly recieved characters to the already available characters of the string
            if door!=None:                                      #When door is empty it will be None else the if statement will get executed.
                size=40-len(door)                               #When we have received all the 40 characters, size will be 0 and the loop terminates
        if ("open" in door) and ("door" in door):               #If the words open and door are present in our received string,
                p.ChangeDutyCycle(10)                           #The door will open by rotating the servo.
        elif ("close" in door) and ("door" in door):            #If the words close and door are present in our received string,
                p.ChangeDutyCycle(5)                            #The door will close by rotating the servo.
        elif (door=="bye".ljust(40)):                           #If the string is "bye", the loop will get terminated
                p.ChangeDutyCycle(5)                            #The door closes back and the program ends
                time.sleep(5)                                   #Waits for 5 seconds before closing the script
                break                                           #
conn.close()                                                    #The connections get closed properly
sock.close()                                                    #
#################################################################
