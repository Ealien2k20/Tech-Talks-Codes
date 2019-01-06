#NOTE:
#The IP address for my raspberry pi and computer will not be the same as yours.
#Make sure that you replace the IP adress in this code with the Local IP address of your Raspbery Pi
#Which can be found by typing ifconfig in terminal

#############################################################Import Essential Libraries
import time                                                 #For manual delays in operations.
import speech_recognition as sr                             #Google's Speech recognition library of python(Requires internet connection)
import socket                                               #For communicating with other devices on the internet
                                                            #
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)       #To work with sockets to communicate on the internet we need to create socket objects which
                                                            #Have the essential function to work with to do networking operations
                                                            #Like sending and recieveing data
sock.connect(("192.168.1.103",4000))                        #Connect our socket with the raspberry pi having Local IP address 192.168.1.103
print("Connected to Raspberry pi Server")                   #Print a message if connection is successful
sr.Microphone(device_index=1)                               #Select the input microphone device for speech recognition (This will work for everyone)
while True:                                                 #Infinite Loop for real time applications
    r=sr.Recognizer()                                       #Create a speech recognition object called r
    r.energy_threshold=5000                                 #Set energy threshold as 5000 to reject background noice and only recognize human voice
    with sr.Microphone() as source:                         #Use the microphone under the name source for the following block of code.
        print("Speak")                                      #A prompt which asks the user to speak.
        audio=r.listen(source)                              #Save the audio data in a object audio
        try:                                                #The code inside 'try' will run and if there is an error due to failure in speech recognition or
                                                            #network error, the except block will be executed
            text=r.recognize_google(audio)                  #Convert the audio to a string and store it in text
            print("You said:"+text)                         #Display the text
            sock.send(text.ljust(40).encode())              #Send the text by altering the string length to 40 by adding blank spaces to raspberry pi 
            if text=="bye":                                 #If the user said bye, the loop will get terminated
                break                                       #Exit the infinite loop
        except:                                             #If an error occurs in try block this block will get executed
            print("Can't recognize")                        #A string saying "Can't recognize" get printed
            time.sleep(5)                                   #Wait for 5 seconds before next voice input can be recorded
                                                            #
sock.close()                                                #Close the connections properly
#############################################################
