import cv2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def mail():
   '''
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    camera.release()
    
    cv2.imwrite('image.jpg', image)
    msg = MIMEMultipart()
    msg['Subject'] = 'Real-time Image'
    msg['From'] = sendr
    msg['To'] = recievr

    # Attach the image to the email
    with open('image.jpg', 'rb') as f:
        img = MIMEImage(f.read())
        msg.attach(img)

    # Send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, 'mxdmymlebttczqbh')
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()
'''

# Set up camera

camera = cv2.VideoCapture(0)

# Take a picture
return_value, image = camera.read()

# Release the camera
camera.release()

# Save the image to your computer
cv2.imwrite('image1.jpg', image)

# Set up email
sender = 'rahulprasad.lower1182@gmail.com'
receiver = 'rahulprasad.lower1182@gmail.com'
msg = MIMEMultipart()
msg['Subject'] = 'Real-time Image'
msg['From'] = sender
msg['To'] = receiver

# Attach the image to the email
with open('image1.jpg', 'rb') as f:
    img = MIMEImage(f.read())
    msg.attach(img)

# Send the email
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender, 'mxdmymlebttczqbh')
server.login(receiver, 'mxdmymlebttczqbh')
server.sendmail(sender, receiver, msg.as_string())
server.quit()
