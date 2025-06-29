import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import os

class SpeechConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech Converter App")
        
        self.init_ui()

    def init_ui(self):
        ttk.Label(self.root, text="Welcome to Speech Converter", font=("Helvetica", 16)).pack(pady=10)

        self.choice_var = tk.StringVar()
        self.choice_var.set("1")

        ttk.Radiobutton(self.root, text="Speech to Text", variable=self.choice_var, value="1").pack()
        ttk.Radiobutton(self.root, text="Text to Speech", variable=self.choice_var, value="2").pack()

        self.language_var = tk.StringVar()
        self.language_var.set("en")

        ttk.Label(self.root, text="Select Language:").pack(pady=(10, 0))
        language_combobox = ttk.Combobox(self.root, textvariable=self.language_var, values=["en", "hi", "pa_IN", "bn"])
        language_combobox.pack(pady=(0, 10))

        self.text_entry = scrolledtext.ScrolledText(self.root, width=40, height=5)
        self.text_entry.pack(pady=(0, 10))

        ttk.Button(self.root, text="Submit", command=self.submit).pack()

    def submit(self):
        choice = self.choice_var.get()

        if choice == "1":
            self.speech_to_text()
        elif choice == "2":
            self.text_to_speech()

    def speech_to_text(self):
        lang = self.language_var.get()

        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Speak Anything :")

            audio = r.listen(source)
            print("Recognizing now....")

            try:
                text = r.recognize_google(audio, language=lang)
                print("You said: " + text)

                with open("text.txt", "w", encoding="utf-8") as file:
                    file.write(text)
                    print("The text saved successfully in the file")

            except sr.UnknownValueError:
                print("Sorry could not understand the audio")

            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service")

    def text_to_speech(self):
        lang = self.language_var.get()
        data = self.text_entry.get("1.0", tk.END).strip()

        text_speech = pyttsx3.init()

        speech = gTTS(data, lang=lang, slow=False)
        speech.save("text.mp3")

        os.system("start text.mp3")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechConverterApp(root)
    root.mainloop()
