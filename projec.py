import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set desired voice properties (optional)
voices = engine.getProperty('voices')  # Get available voices
engine.setProperty('voice', voices[0].id)  # Set the voice (0 for male, 1 for female)
engine.setProperty('rate', 150)  # Set speech rate

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()
    

# Example usage
speak("Hello, world!")
speak("This is an example of text-to-speech in Python.")
      






import speech_recognition as sr

# Initialize recognizer
r = sr.Recognizer()

# Function to recognize speech from microphone
def recognize_speech_to_text():
    with sr.Microphone() as source:
        print("Speak now:")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print("You said:", text)

            
return text
        except sr.UnknownValueError:
            print("Could not understand audio")

            
return
 
""

        
except sr.RequestError as e:
            print("Could not request results from speech recognition service; {0}".format(e))
            return ""

# Example usage
text = recognize_speech_from_mic()
print(text)