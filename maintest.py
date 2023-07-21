from email.message import EmailMessage
import face_recognition
import cv2
import pyttsx3
import datetime
import gtts
import time
import pyrebase
from playsound import playsound
import smtplib
import imghdr
import os
import numpy as np
import platform
import speech_recognition as sr
#import capture


class project:
    def image_saver(self):
        try:
            face_cascade = cv2.CascadeClassifier(
                './Python_code\haarcascade_frontalface_default.xml')
            video = cv2.VideoCapture(0)
            check, frame = video.read()
            video.release()
            cv2.imwrite('image1.jpg', frame)
            #mirrored_frame = cv2.flip(frame,1)
            #out.write(mirrored_frame)
            
        except:
            print('WebCam Is Not Working Properly or Plugged In1.')

    def update_to_null(self):
        firebaseConfig = {
            "apiKey": "AIzaSyCBEBT_WywV1wym_xmH-AafzhBzh1qAZRE",
            "authDomain": "security-system-9a042.firebaseapp.com",
            "databaseURL": "https://security-system-9a042-default-rtdb.firebaseio.com/",
            "projectId": "security-system-9a042",
            "storageBucket": "security-system-9a042.appspot.com",
            "messagingSenderId": "657594533352",
            "appId": "1:657594533352:web:b91a66962504ae96b5105d",
            "measurementId": "G-KQSKLRNLBG"
        }

        firebase = pyrebase.initialize_app(firebaseConfig)
        db = firebase.database()
        db.child("permission").update({"unlock": "null"})

    def takeresponse(self):
        firebaseConfig = {
            "apiKey": "AIzaSyCBEBT_WywV1wym_xmH-AafzhBzh1qAZRE",
            "authDomain": "security-system-9a042.firebaseapp.com",
            "databaseURL": "https://security-system-9a042-default-rtdb.firebaseio.com/",
            "projectId": "security-system-9a042",
            "storageBucket": "security-system-9a042.appspot.com",
            "messagingSenderId": "657594533352",
            "appId": "1:657594533352:web:b91a66962504ae96b5105d",
            "measurementId": "G-KQSKLRNLBG"
        }
        firebase = pyrebase.initialize_app(firebaseConfig)
        db = firebase.database()
        value = db.child("permission").child("unlock").get()
        print(value.val())
        return value.val()

    def email(self, mesg, ph):
        
        EMAIL_ADDRESS = "rahulprasad.lower1182@gmail.com"
        EMAIL_PASSWORD = 'mxdmymlebttczqbh'
        msg = EmailMessage()
        msg['Subject'] = 'Intruder Alert!'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg.set_content('Do you want to let him in?\nReason: '+mesg+'\nPhone number : '+ph +
                        "\nPlease give your response\n https://rahul-1182.github.io/Security-System-sem-6/")
        with open('image1.jpg', 'rb') as f:
            image_data = f.read()
            image_type = imghdr.what(f.name)
            image_name = f.name
        msg.add_attachment(image_data, maintype='image',
                           subtype=image_type, filename=image_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

    def GetInput(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source, 15)
        try:
            print(r.recognize_google(audio))
            command = r.recognize_google(audio)
        except sr.UnknownValueError:
            print('Unable To UnderStand')
            command = ''
        except sr.RequestError as e:
            print('Google Says error: {}'.format(e))
            command = ''
        finally:
            return command

    def getWords(self, sentence):
        ls = sentence.split()
        sentence = ""
        sentence = sentence.join(ls)
        return sentence

    def response_taker_first(self):
        name = 'Unknown'
        self.speak("unknown visitor asking for permission")
        self.speak("please tell the reason for visiting")
        msg = self.GetInput()
        print(msg)
        self.speak("please speak your phone number")
        ph = self.GetInput()
        ph = self.getWords(ph)
        self.email(msg, ph)
        t_end = time.time() + 60
        flag = False
        while time.time() < t_end:
            response = self.takeresponse()
            if (response == "yes"):
                self.speak('You Can Go Inside the House')
                self.update_to_null()
                flag = True
                break
            if (response == "no"):
                self.speak("Sorry you are not allowed to go inside ")
                self.update_to_null()
                flag = True
                break
        if (flag == False):
            self.speak("Sorry you can come later as onwer is busy right now")
            now = datetime.datetime.now()
            cur = cv2.imread('./Python_code/visitor/visitor.jpg')
            cv2.imwrite('./Python_code/Unattended/savedImage.jpg', cur)
            image_time = now.strftime("%m-%d-%Y__%H-%M-%S") + '.jpg'
            image_name = "./Unattended/" + image_time
            os.rename("./Python_code/Unattended/savedImage.jpg", image_name)
        return name

    def recogonizer(self, encodeListKnown, images, classNames):
        cur = cv2.imread('./Python_code/visitor/visitor.jpg')
        imgSmall = cv2.resize(cur, (0, 0), None, 0.25, 0.25)
        imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(imgSmall)
        encodesCurFrame = face_recognition.face_encodings(
            imgSmall, facesCurFrame)
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(
                encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(
                encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                for i in range(3):
                    password = input('Give the password via keyboard:')
                    if (password == '1234'):
                        self.speak('welcome door unlocked')
                        return name
                self.speak('Something seems to be fishy')
                return self.response_taker_first()
            else:
                return self.response_taker_first()

    def webcam(self):
        '''Detecting Webcam and Making Rectangles on it.'''
        try:
            face_cascade = cv2.CascadeClassifier(
                './Python_code\haarcascade_frontalface_default.xml')
            video = cv2.VideoCapture(0)
            now = time.time()
            while (time.time() < (now+10)):
                check, frame = video.read()
                faces = face_cascade.detectMultiScale(
                    frame
                )
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, 'Please Be Inside The Frame', (40, 35),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 3)
                cv2.imshow('Video', frame)
                cv2.waitKey(1)
            video.release()
            cv2.destroyAllWindows()
        except:
            print('WebCam Is Not Working Properly or Plugged In2.')

    def greeting(self):
        curr_time = datetime.datetime.now()
        curr_time = str(curr_time.hour).zfill(2)+str(curr_time.minute).zfill(2)
        if (curr_time > '0000' and curr_time <= '1159'):
            self.speak('Good Morning')
        elif (curr_time <= '1700'):
            self.speak('Good AfterNoon')
        else:
            self.speak('Good Evening')

    def speak(self, saying):
        if (platform.system() == 'Linux'):
            tts = gtts.gTTS(saying)
            tts.save('./visitor/voice.mp3')
            playsound('./visitor/voice.mp3')
        else:
            engine = pyttsx3.init()
            engine.setProperty('rate', 170)
            engine.say(saying)
            engine.runAndWait()

    def autodetect(self):
        try:
            face_cascade = cv2.CascadeClassifier(
                './Python_code\haarcascade_frontalface_default.xml')
            video = cv2.VideoCapture(0)
            # print(ok)
            while True:
                check, frame = video.read()
                faces = face_cascade.detectMultiScale(
                    frame
                )
                if (len(faces) == 0):
                    return False
                else:
                    return True
        except:
            print('WebCam Is Not Working Properly or Plugged In3.')

    def findEncodings(self, images):
        encodeList = []
        for i in images:
            i = cv2.cvtColor(i, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(i)[0]
            encodeList.append(encode)
        return encodeList

    def load_encodings(self):
        path = 'Python_code\TestImages'
        images = []
        classNames = []
        myList = os.listdir(path)
        print(myList)
        for i in myList:
            curImg = cv2.imread(f'{path}/{i}')
            images.append(curImg)
            classNames.append(os.path.splitext(i)[0])
        print(classNames)
        encodeListKnown = self.findEncodings(images)
        print('Encoding Complete')
        return encodeListKnown, images, classNames

    def main(self):
        while (True):
            if (self.autodetect()):
                encodeListKnown, images, classNames = self.load_encodings()
                self.greeting()
                self.speak('hi i am your virtual assisstant')
                self.webcam()
                if (self.autodetect()):
                    self.image_saver()
                    name = self.recogonizer(
                        encodeListKnown, images, classNames)
                    print(name)
                self.speak('Bye')
                time.sleep(30)
            else:
                time.sleep(1)


if __name__ == '__main__':
    obj = project()
    obj.main()
