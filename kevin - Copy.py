import datetime
import os
import smtplib
import sys
import webbrowser
import operator
import cv2
import pyttsx3
import pywhatkit as kit
import requests
import speech_recognition as sr
import wikipedia
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtCore import QDate, Qt, QTime, QTimer
from PyQt5.QtGui import *
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from requests import get 
from bs4 import BeautifulSoup 
from pywikihow import search_wikihow
import speedtest
from DATAUI import Ui_MainWindow

engine = pyttsx3.init('sapi5')
voices= engine.getProperty('voices') 

engine.setProperty('voice', voices[0].id)
def speak(audio):
    engine.say(audio) 
    engine.runAndWait() 
def sendEmail(to , body):
      server = smtplib.SMTP('smtp.gmail.com', 587)
      server.ehlo()
      server.starttls()
      server.login('nakshatramanglik14@gmail.com','naksh14142003')
      server.sendmail('nakshatramanglik14@gmail.com',to, body)
      server.close()

def wishme():
        hour=int(datetime.datetime.now().hour)
        if hour>= 0 and hour <12 :
             speak("Good morning sir !")
             print("Good morning sir !")

        elif hour >=12 and hour <18 :
             speak("Good Afternoon sir!")
             print("Good Afternoon sir!")
        else:
             speak ("Good evening sir !")
             print("Good evening sir !")        
        speak(" I am kevin.... How may i help you sir ! ")
        print("I am kevin.... How may i help you sir !")
class MainThread(QThread):
      def __init__(self) :
            super(MainThread,self).__init__()
      def run(self) :
            self.TaskExecution()  
            
      def takeCommand(self):
            r=sr.Recognizer()
            with sr.Microphone() as source:
                  print ("listening....!")
                  r.pause_threshold = 1
                  audio =r.listen(source,timeout=4,phrase_time_limit=7)
            try:
                  print("Recognising....!")
                  query =r.recognize_google(audio,language="en-in")
                  print (f"user said : {query}\n" )
            except Exception as e :
                  
                  print ("Say that again plz .....")
                  speak("please say that again !")
                  return "None"
            return query       
            

      def TaskExecution(self) :
             wishme()
             while True :
                  self.query = self.takeCommand()
                  if "open Notepad" in self.query or "Notepad" in self.query :
                        path='C:\\Windows\\system32\\notepad.exe'
                        os.startfile(path)
                        speak('opening notepad')
                        print ('opening notepad')
                  elif "command prompt" in self.query or "cmd" in self.query :
                        os.system('start cmd ')
                  elif "take picture" in self.query :
                        cap = cv2.VideoCapture(0)
                        while True :
                              ret, img = cap.read()
                              cv2.imshow('webcam',img)
                              k = cv2.waitKey(50)
                              if k == 27 :
                                    break;
                        cap.release()
                        cv2.destrAllWindows()
                  elif "IP Address" in self.query or "address" in self.query:
                        ip = get('https://api.ipify.org').text
                        speak (f"your IP address is {ip}") 
                        print (ip)    
                  elif "Wikipedia" in self.query:
                        speak ("searching wikipedia.... ")
                        query=self.query.replace("wikipedia","")
                        results= wikipedia.summary(query,sentences=2 )
                        speak("according to wikipedia")
                        print(results)
                        speak (results) 

                  elif "open YouTube" in self.query or "YouTube" in self.query :
                        webbrowser.open("youtube.com")
                        speak("opening youtube !")
                  elif "open Google" in self.query or "search" in self.query :
                        speak ("what should i search on google sir ?")
                        cm = self.takeCommand().lower()
                        webbrowser.open(f"{cm}")
                        speak ("opening google ")
                  elif "open Firefox" in self.query:
                        codePath='C:\\Users\\naksh\\OneDrive\\Desktop'
                        os.startfile(codePath)
                        speak ('opening firefoox !')
                        print ("opening firefox !")
                  elif "open Whatsapp" in self.query or "Whatsapp" in self.query:
                        webbrowser.open("whatsapp.com")
                        speak ("opening whatsapp")
                        print ("opening whatsapp")
                  elif "open Instagram" in self.query or "Instagram" in self.query :
                        webbrowser.open("instagram.com") 
                        speak ("opening instagram")
                        print ("opening instagram")
                  elif "play songs on" in self.query or "songs" in self.query or "song" in self.query :
                        kit.playonyt("night changes")
                  elif "email to person" in self.query :
                        try :
                              speak ("what should i write ?") 
                              body = self.takeCommand().lower()
                              to = "prachimanglik37@gmail.com"
                              sendEmail = (to, body)  
                              speak ("email has been delivered")

                        except Exception as e :
                              print(e)
                              speak("sorry sir , i am not able to deliver your email ")
                  elif "where I am" in self.query or "where are we" in self.query or "locate me" in self.query :
                        speak("wait sir let me check!")
                        try:
                              ip = requests.get("https://api.ipify.org").tect
                              print(ip)
                              location = "https://get.geojs.io/v1/ip/geo" + ip + '.json'
                              geo_requests = requests.get(location)
                              geo_data = geo_requests.json()
                              town = geo_data['town']
                              country = geo_data['country']
                              speak (f"sir i am not sure about exact location but for approximation we are in {town} city of {country} ")
                        except Exception as e:
                              speak("sorry sir due to network issue i am not able to locate you ! forgive me sir.")
                              pass
                  elif "do some calculations" in self.query or "can you calculate" in self.query or "calculate" in self.query :
                        try :
                            r= sr.Recognizer()
                            with sr.Microphone() as source :
                                  speak ("what do you want to calculate ?")
                                  print ("listening!.....")
                                  r.adjust_for_ambient_noise(source)
                                  audio = r.listen(source)
                            my_string = r.recognize_google(audio)
                            print(my_string)
                            def get_operator_fn(op):
                                return{
                                       '+': operator.add,
                                       '-': operator.sub,
                                       '*': operator.mul,
                                       'divided': operator.__truediv__,
                              
                                     }  [op] 
                            def eval_binary_expr(op1,oper,op2):
                                op1 , op2 = int(op1),int(op2)
                                return get_operator_fn(oper)(op1,op2)
                            speak("your result is")
                            speak(eval_binary_expr(*(my_string.split)))      


                        except Exception as e :
                              print("there is some error while calculating the problem..")
                  elif "uber" in self.query or "book uber" in self.query :
                        webbrowser.open("uber.com")    
                        speak("opening uber website")
                        print("opening uber")        
                              


                  
                  
                  elif 'play music' in self.query or "music" in self.query :
                        webbrowser.open("spotify.com") 
                        speak ("opening music player") 
                        print ("opening music player !")

                  elif 'vs code' in self.query : 
                        codePath ="C:\\Users\\naksh\\AppData\\Local\\Programs\\Microsoft VS Code\\code.exe" 
                        os.startfile(codePath)
                        speak ("opening vs code")

                  
                  elif 'no thank you' in self.query or "no" in self.query or "stop" in self.query or "nothing else" in self.query :
                        speak("i am taking off ! take care sir")
                        print("i am taking off ! take care sir")
                        sys.exit()
                  elif "hi" in self.query or "hey" in self.query or "hello" in self.query :
                        speak("hi sir , i am kevin ...")  
                  elif "how are you ?" in self.query or "how you doing?" in self.query or "whats about you ?" in self.query:
                        speak("i am fine sir.what about you  ")  
                  elif "good morning" in self.query :
                        speak("good morning sir")  
                  elif "good afternoon" in self.query:
                        speak("good afternoon sir")  
                  elif "fine" in self.query or "i am good" in self.query or "great" in self.query:
                        speak("thats great to hear from you") 
                  elif "not fine" in self.query or "not good" in self.query:
                        speak("everything will work out sir . dont worry!")
                  elif"thank you" in self.query :
                        speak ("you are welcome sir ")
                  elif "temperature" in self.query:
                        search = "temperature in ghaziabad"
                        url = f"https://www.google.com/search?q={search}" 
                        r = requests.get(url)  
                        data = BeautifulSoup(r.text,"html.parser")
                        temp = data.find("div", class_="BNeawe").text
                        speak(f"current{search} is {temp}")
                  elif "speed test" in self.query or "speed" in self.query or "internet speed" in self.query  or "test" in self.query:
                        t = speedtest.Speedtest()
                        d = t.download()
                        u = t.upload()
                        speak(f"sir you have {d} bits per second downloading speed and {u} bits per second uploading speed ")
                        print(f"donload = {d} and upload ={u} ")
                        
                  elif "activate" in self.query or "wait"in self.query:
                        
                     speak("how to do mod is activated") 
                     while True :
                         speak ("please tell me what do you want to know") 
                         how = self.takeCommand().lower()
                         try: 
                              if "exit" in how or "close" in how :
                                    speak("ok sir  how to mod is closed ")
                                    break
                              else:
                                    max_results = 1
                                    how_to = search_wikihow(how,max_results)
                                    assert len(how_to)== 1
                                    how_to[0].print()
                                    speak(how_to[0].summary)     
                         except Exception as e :
                               speak("sorry sir , i am not able to find this .")                         

                  speak("do you have any other work ?")
startExecution = MainThread()

class Main(QMainWindow):
      def __init__(self):
            super().__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.ui.pushButton.clicked.connect(self.startTask)
            self.ui.pushButton_2.clicked.connect(self.close)
      def startTask (self):
            self.ui.movie = QtGui.QMovie("../jarvis/2022-11-15 (5).png") 
            self.ui.label.setMovie(self.ui.movie)
            self.ui.movie.start()
            self.ui.movie = QtGui.QMovie("../jarvis/2022-11-15 (1).png") 
            self.ui.label.setMovie(self.ui.movie)
            self.ui.movie.start()
            timer = QTimer(self)
            timer.timeout.connect(self.showTime)
            timer.start(10000)
            startExecution.start()
            
      def showTime(self):
            current_time = QTime.currentTime()
            now = QDate.currentDate()
            label_time = current_time.toString('hh:mm:ss')
            label_date = now.toString(Qt.ISODate)
                
app = QApplication(sys.argv)
kevin = Main()
kevin.show()
exit(app.exec_())             




                   