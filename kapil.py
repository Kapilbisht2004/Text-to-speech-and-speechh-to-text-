import speech_recognition as sp
import pyttsx3
from gtts import gTTS
import os
import sys
print("\t\t Welcome to speech to text and text to speech conversion software")
print("1- To convert speech to text press : a \n2- To convert text to speech press : b")
fun = input("enter your choice : ")

def speech_to_text():
    print("1- To speak in English press : 1")
    print("2- To speak in Hindi press : 2")
    print("3- To speak in Punjabi press : 3")
    print("4- To speak in bhojpuri press : 4")
    print("5- To speak in bengali press : 5")
    print("6- To exit press : *")
    lang = input('Please enter your choice : ')
        
    while(lang!='*'):
        r = sp.Recognizer()
        
        with sp.Microphone() as source:
            
            r.adjust_for_ambient_noise(source)
            print("Speak Anything :")
            
            audio = r.listen(source)
            print("recognizing now....")
            
            try:
                if lang=='1':
                    text=r.recognize_google(audio, language='en')
                elif lang=='2':
                    text = r.recognize_google(audio, language="hi")
                elif lang=='3':
                    text = r.recognize_google(audio, language="pa_IN")
                elif lang=='4':
                    text = r.recognize_google(audio, language="hi")
                elif lang=='5':
                    text = r.recognize_google(audio, language="bn")
                elif lang=='*':
                    text=r.recognize_google(audio, language='en')
                print("You said : "+text )
                
            except sp.UnknownValueError:
                print("Sorry could not understand the audio")
                
            except sp.RequestError as e:
                print("Could not request results from Google Speech Recognition service")
                
            with open("text.txt","w",encoding="utf-8") as file:
                file.write(text)
                print("The text saved successfully in the file")
                
            lang = input('Enter the number of your language: ')
            
    file.close()

def text_to_speech():
        print("1- If you want to enter the text to be converted to speech press : e\n2- If if do not want to enter the text press : f")
        choice=input("Enter the choice : ")
        
        text_speech=pyttsx3.init()
        
        if choice=='f':
            with open("text.txt","r",encoding="utf-8") as file:
                data = file.read().strip()
        elif choice=='e':
                data=input("Enter the text : ")
                
        print("Text to be converted into speech is : ")
        print(data)
        
        speech = gTTS(data, lang='hi', slow=False)
        speech.save("text.mp3")

        os.system("start text.mp3")
        file.close()

if fun=='a':
    speech_to_text()
elif fun=='b':
    text_to_speech()
else:
    print("wrong choice entered")