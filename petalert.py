import time
import serial
import smtplib

TO = '[RECIPIENT EMAIIL HERE]'
GMAIL_USER = '[SENDER EMAIL HERE]'
GMAIL_PASS = '[SENDER EMAIL APP PASSWORD HERE]'

SUBJECT_DEFAULT = 'First Motion Detected'
BODYTEXT_DEFAULT = 'Motion has been detected at the dog door.'
SUBJECT_TEMP = 'Temperature Alert First Motion Detected'
BODYTEXT_TEMP = 'Motion has been detected at the dog door. Ambient temperature is above threshold.'
SUBJECT_SECONDMOTION = 'Second Motion Missed'
BODYTEXT_SECONDMOTION = 'Motion has not been detected at your dog door since first motion. Please check on your dog.'
  
ser = serial.Serial('COM3', 9600)

def send_email_default():
    print("Sending Email")
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(GMAIL_USER, GMAIL_PASS)
    header = 'To:' + TO + '\n' + 'From: ' + GMAIL_USER
    header = header + '\n' + 'Subject:' + SUBJECT_DEFAULT + '\n'
    print(header)
    msg = header + '\n' + BODYTEXT_DEFAULT + ' \n\n'
    smtpserver.sendmail(GMAIL_USER, TO, msg)
    smtpserver.close()
    
def send_email_temp_alert(temp1, temp2):
    print("Sending Temp Email")
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(GMAIL_USER, GMAIL_PASS)
    header = 'To:' + TO + '\n' + 'From: ' + GMAIL_USER
    header = header + '\n' + 'Subject:' + SUBJECT_TEMP + '\n'
    print(header)
    msg = header + '\n' + BODYTEXT_TEMP + '\n'
    msg = msg + '\n' + 'Temperature Threshold: ' + temp1 + ' F' + '\n'
    msg = msg + '\n' + 'Ambient Temperature: ' + temp2 + ' F' + ' \n\n'
    smtpserver.sendmail(GMAIL_USER, TO, msg)
    smtpserver.close()
    
def send_email_second_motion():
    print("Sending Second Motion Email")
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(GMAIL_USER, GMAIL_PASS)
    header = 'To:' + TO + '\n' + 'From: ' + GMAIL_USER
    header = header + '\n' + 'Subject:' + SUBJECT_SECONDMOTION + '\n'
    print(header)
    msg = header + '\n' + BODYTEXT_SECONDMOTION + ' \n\n'
    smtpserver.sendmail(GMAIL_USER, TO, msg)
    smtpserver.close()
    
while True:
    message = ser.readline()
    message = message.decode('utf-8')
    print(message)
    if message[0:4] == "MOVE":
        send_email_default()
    if message[0:4] == "TEMP":
        splitMessage = message.split(",")
        tempThreshold = splitMessage[1]
        ambientTemp = splitMessage[2]
        ambientTemp = ambientTemp[0:-2]
        send_email_temp_alert(tempThreshold, ambientTemp)
    if message[0:4] == "SECO":
        send_email_second_motion()
    time.sleep(0.15)
