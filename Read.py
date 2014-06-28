import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected: Type " +str(TagType)
    
        ## Get the UID of the card (also selects card)  
        (status,uid) = MIFAREReader.MFRC522_GetUID()
                       
        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
          
            # Print UID
            uidh = map(hex, uid)
            uidh = map(str, uidh)
            
            print "UID Length: "+str(len(uid))
            print "Card read UID: "+ ", ".join(map(str,uid))
            print "Card read HEX: "+ ", ".join(uidh)
        
            # Select key for authentication
            key = MIFAREReader.defaultKeyA

            # Authenticate
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

            # Check if authenticated
            if status == MIFAREReader.MI_OK:
                MIFAREReader.MFRC522_Read(8)
                MIFAREReader.MFRC522_StopCrypto1()
            else:
                print "Authentication error"

            # Stop scanning for cards
            continue_reading = False
        
        #Tidy up GPIO
        GPIO.cleanup()
