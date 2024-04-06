# main.py program to automatically capture pictures when time trigger expires
# modify /etc/rc.local by adding commands to automatically execute the program
# Add these commands to rc.local
# sudo python3 /home/Desktop/PythonWorkSpace/FlightLightCam/main.py &

import time
import cv2 as cv
import os
import logging

# create the objects that point to the cameras
cam1 = cv.VideoCapture(0)
#cam2 = cv.VideoCapture(2)

timeToTakeImage = 1       # trigger for how many seconds until take image
imageNumber     = 0       # used in filename to store image
error_log_file  = "/home/pi/Desktop/Error_Logs/log.log"
directoryPath   = "/home/pi/Desktop/"
directoryName   = "FT"
directoryNumber = 0

logging.basicConfig(level=logging.DEBUG, filename=error_log_file)
startTime = time.time()
endTime   = time.time()
timeDiff  = 0

if cam1.isOpened():
    # check whether the directory already exists to write images into
    while (os.path.exists(directoryPath+directoryName+ str(directoryNumber))):
        directoryNumber = directoryNumber + 1
    
    # this is the directory to write to    
    finalDirectory = directoryPath+directoryName+str(directoryNumber)+"/"
    os.mkdir(finalDirectory)
    
    while(True):
        # calculate how much time has passed
        timeDiff = endTime - startTime
        
        if(timeDiff > timeToTakeImage):
            # threshold of time has passed so take pictures
            timeDiff = 0
            startTime = time.time()
            
            # capture a frame from camera 1 and write to file
            ret1, frame1 = cam1.read()
            
            # if ret1 is True then we successfully grabbed a frame
            if(ret1):
                fileName1 = "Cam1-Ft2-" + str(imageNumber) + ".jpg"
                cv.imwrite(finalDirectory+fileName1, frame1)
            else:
                error_string = str(startTime) + ":" + "Trouble grabbing frame"
                logging.warning(error_string)
                
            #  increment the number of images taken
            imageNumber = imageNumber + 1
        
        # get system time
        endTime = time.time()
    # end of if
    
else:
    # log to the error file so that it can be debugged later
    error_string = str(startTime) + " : " + "can't open camera on start up"
    logging.critical(error_string)

# release the object 
cam1.release()

# end of program