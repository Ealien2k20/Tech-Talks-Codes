#Note:
#1)The IP Address in the code should be replaces with yours.
############################IMPORT LIBRARIES#####################################
import socket                                                                   #For communicating with devices in the LAN.
import cv2                                                                      #For Image processing.
import numpy as np                                                              #For matrix operations.
#####################FUNCTION TO GET IMAGES FROM NETWORK#########################
def recvall(sock, count):                                                       #This function retrieves the images from Raspberry Pi over LAN.
                                                                                #Sock is the socket object to get data from Raspberry Pi and count is the number of characters to be received.
    buf = b''                                                                   #Initialise an empty buffer to store the recieved byte stream.
    while count:                                                                #Loop for reliable data transfer (Obtain data till count=0).
        newbuf = sock.recv(count)                                               #Get the string from Raspberry Pi
        if not newbuf: return None                                              #If nothing is received, return None.
        buf += newbuf                                                           #Append recieved characters to empty buffer.
        count -= len(newbuf)                                                    #Reduce count by number of characters recieved. If all characters are recieved,
                                                                                #Count becomes zero.
    return buf                                                                  #Return the received byte stream.
###################CONNECTING TO RASPBERRY PI####################################
TCP_IP = '192.168.1.104'                                                        #IP address of Raspberry Pi.
TCP_PORT = 40000                                                                #Communication through port 40000.
face_casc=cv2.CascadeClassifier("Cascades/haarcascade_frontalface_default.xml") #Trained xml file for face detection stored in Cascades folder.
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                        #Creating socket object. AF_INET => IPV4, SOCK_STREAM => BYTE STREAM.
conn.connect((TCP_IP, TCP_PORT))                                                #Connect to Raspberry Pi.
face_cent=320                                                                   #When no Face is detected, face center is taken as 320.
#########################MAIN LOOP###############################################
while True:                                                                     #Infinite loop for face detection.
    length = recvall(conn,16)                                                   #Receive the number of characters to be received first(This data is 16 characters long).
    stringData = recvall(conn, int(length))                                     #stringData is the received byte Stream.
    data = np.frombuffer(stringData, dtype='uint8')                             #Convert byte stream to numpy array(typical image).
    frame=cv2.imdecode(data,1)                                                  #Decode the array to make it as a compatible image.
    faces=face_casc.detectMultiScale(frame)                                     #Detect the faces in the recieved image using the xml file
    for x,y,w,h in faces:                                                       #For the face coordinates in received face coordinates
        face_cent=x+w//2                                                        #Calculate the center of the face.
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),10)                       #Draw a rectangle enclosing the face.
        break                                                                   #Terminate the loop.
    pos=str(face_cent).ljust(10)                                                #Convert the face center into a string of length 10.
    conn.send(pos.encode())                                                     #Send it back to Raspberry Pi.
    cv2.imshow("Frame",frame)                                                   #Display the recieved image with detected face.
    if cv2.waitKey(1)==27:                                                      #Keyboard interrupt.
        break                                                                   #Terminate the loop.
conn.send("bye".ljust(10).encode())                                             #Sending a bye message to Raspberry Pi if program ends and closing connections.
conn.close()                                                                    #
cv2.destroyAllWindows()                                                         #Closes the image window.
#################################################################################
