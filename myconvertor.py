import tkinter as tk
from tkinter import ttk, scrolledtext
import speech_recognition as sr
from gtts import gTTS
import os

class SpeechConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech Converter App") 

        self.init_ui()  # Initialize the user interface

    def init_ui(self):
        ttk.Label(self.root, text="Welcome to Speech Converter", font=("Helvetica", 16)).pack(pady=10)

        # Create a StringVar to hold the user's choice between Speech to Text and Text to Speech
        self.choice_var = tk.StringVar()
        self.choice_var.set("1")  

        
        ttk.Radiobutton(self.root, text="Speech to Text", variable=self.choice_var, value="1").pack()
        ttk.Radiobutton(self.root, text="Text to Speech", variable=self.choice_var, value="2").pack()

        # Create a StringVar to hold the selected language
        self.language_var = tk.StringVar()
        self.language_var.set("English")  

    
        ttk.Label(self.root, text="Select Language:").pack(pady=(10, 0))
        
        # Create and pack a combobox for selecting the language
        language_combobox = ttk.Combobox(self.root, textvariable=self.language_var, values=["English", "Hindi", "Punjabi", "Bengali"])
        language_combobox.pack(pady=(0, 10))

        # Create and pack a scrolled text widget for displaying or entering text
        self.text_entry = scrolledtext.ScrolledText(self.root, width=40, height=5)
        self.text_entry.pack(pady=(0, 10))

        # Create and pack a button that triggers the submit action
        ttk.Button(self.root, text="Submit", command=self.submit).pack()

    def submit(self):
        choice = self.choice_var.get()

        if choice == "1":
            self.speech_to_text()  
        elif choice == "2":
            self.text_to_speech()  

    def speech_to_text(self):
        # Map language names to their corresponding codes for the Google Speech Recognition API
        lang_map = {
            "English": "en",
            "Hindi": "hi",
            "Punjabi": "pa-IN",
            "Bengali": "bn"
        }
        # Get the language code based on the user's selection
        lang = lang_map[self.language_var.get()]

        # Initialize the recognizer
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)  
            print("Speak Anything :") 
            audio = r.listen(source)  
            print("Recognizing now....")  
            try:
                # Recognize the speech using Google Web Speech API
                text = r.recognize_google(audio, language=lang)
                print("You said: " + text)  

                # Display the recognized text in the scrolled text widget
                self.text_entry.delete("1.0", tk.END)
                self.text_entry.insert(tk.END, text)

            except sr.UnknownValueError:
                print("Sorry, could not understand the audio") 

            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service")  

    def text_to_speech(self):
    
        lang_map = {
            "English": "en",
            "Hindi": "hi",
            "Punjabi": "pa",
            "Bengali": "bn"
        }
        lang = lang_map[self.language_var.get()]
        # Get the text from the scrolled text widget
        data = self.text_entry.get("1.0", tk.END).strip()

        # Convert the text to speech using Google Text-to-Speech API
        speech = gTTS(data, lang=lang, slow=False)
        
        speech.save("text.mp3")

        os.system("start text.mp3")

if __name__ == "__main__":
    root = tk.Tk()  
    app = SpeechConverterApp(root)  
    root.mainloop()  # Start the Tkinter event loop
