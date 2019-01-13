#Note:
#1)The IP Address in the code should be replaces with yours.
#2)Visit previous week programs to know more about socket and Servo.
##########################LIBRARIES##################################
import cv2                                                          #For Image Processing.
import numpy as np                                                  #For Matrix Operations.
import RPi.GPIO as GPIO                                             #For controlling GPIO pins.
import socket                                                       #For communicating with computer.
##########################INITIALISATION#############################
GPIO.setwarnings(False)                                             #Ignore warnings due to unproperly closed previous scripts.
GPIO.setmode(GPIO.BOARD)                                            #Select the PIN cofiguration for Raspi visit previous scripts for more details about.
                                                                    #GPIO and Servo motors.
GPIO.setup(12,GPIO.OUT)                                             #Set 12th pin as output pin for Servo.
p=GPIO.PWM(12,50)                                                   #Frequency of PWM is set as 50 Hz.
p.start(7.5)                                                        #Start cycles at 12th pin with duty cycle 5.
TCP_IP = '192.168.1.104'                                            #IP Address of Raspberry Pi.
TCP_PORT = 40000                                                    #Communcation through port 40000.
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)                #Creating socket object for Raspberry Pi.
s.bind((TCP_IP, TCP_PORT))                                          #Associate the Raspiberry Pi's IP and Port to the socket object.
s.listen(5)                                                         #Waits for devices to connect.
print("Connect")                                                    #Prompts for devices to connect.
sock,ip = s.accept()                                                #Accepts a device and sock is an object to communicate with that device.
print("Connected")                                                  #Prints the message Connected if a successful connection is established.
cap=cv2.VideoCapture(0)                                             #Create Video Capture Object for Web camera for getting images continuosly.
face_cascade=cv2.CascadeClassifier("Cascades/face.xml")             #Trained File to Detect Faces.
duty=7.5                                                            #Initial Duty Cycle.
##########################MAIN LOOP##################################
while True:                                                         #Infinite Loop to send images to Laptop(Client).
    ret,frame=cap.read()                                            #Retrieve and image from the camera.
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]                 #Encoding parameter for the image.
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)   #Encodes the image using the parameter.
    data = np.array(imgencode)                                      #Converts encoded image to a single numpy array.
    stringData = data.tostring()                                    #Convert the numpy array to a string.
    sock.send(( str(len(stringData)).ljust(16)).encode());          #Send the length of the String to the Laptop first so that it can receive the image reliably.
    sock.send( (stringData));                                       #Sends the actual string.
####################RECEIVING FACE DATA FROM CLIENT##################
    size=10                                                         #Size of face data will be 10 characters long.
    pos=""                                                          #pos is an empty string to hold the received face data.
    while(not size==0):                                             #Loop for reliable data transfer.
        data=sock.recv(10).decode()                                 #Obtain 10 characters from Raspbery Pi.
        pos+=data                                                   #Append received characters to pos
        size-=len(data)                                             #Decrease size by the number of received characters. If all characters are received,size will be equal to 0.
    if pos=="bye".ljust(10):                                        #If Client sends bye, terminate the program as CLIENT has disconnected.
        break                                                       #Terminate the current loop.    
    face_cent=int(pos)                                              #Convert the recieved string to an integer which holds face center position.
    if face_cent>=370:                                              #Checks if face's center is on the right, if so rotate the servo clockwise.
        duty-=0.025                                                 #To rotate clockwise, reduce duty cycle.
    elif face_cent<=270:                                            #Checks if face's center is on the left, if so rotate the servo anti-clockwise.
        duty+=0.025                                                 #To rotate anti-clockwise, increase duty cycle.
    p.ChangeDutyCycle(duty)                                         #Rotate servo with calculated duty cycle.                            
#########################TERMINATION#################################
GPIO.cleanup()                                                      #Clear the GPIO Pins.
sock.close()                                                        #Close the connections.
s.close()                                                           #
#####################################################################
