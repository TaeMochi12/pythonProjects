import tempfile
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import tkinter as tk
from tkinter import messagebox
import pygame


# Function to handle the speech recognition and translation
def process_speech():
    try:
        with sr.Microphone() as source:
            print("Speak now!")
            audio = r.listen(source)

        speech_text = r.recognize_google(audio)
        print(speech_text)

        if speech_text == "exit":
            root.destroy()  # Close the GUI window
            return

        translated_text = translator.translate(speech_text, dest="hi")
        translated_text_only = translated_text.text

        print(translated_text_only)

        speech_text_box.insert(tk.END, f"Recognized Text: {speech_text}\n")
        translated_text_box.insert(
            tk.END, f"Translation: {translated_text_only}\n")

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            voice_file = temp_file.name
            temp_file.close()

            voice = gTTS(translated_text_only, lang="hi")
            voice.save(voice_file)

            pygame.mixer.init()
            pygame.mixer.music.load(voice_file)
            pygame.mixer.music.play()

    except sr.UnknownValueError:
        messagebox.showinfo("Error", "Could not understand.")

    except sr.RequestError:
        messagebox.showinfo("Error", "Could not understand.")


# Function to handle the keyboard interrupt
def handle_interrupt():
    root.destroy()  # Close the GUI window


# Create the main window
root = tk.Tk()
root.title("Speech Translation")

# Create GUI elements
label = tk.Label(root, text="Speak now and click Translate:")
label.pack()

speech_text_box = tk.Text(root, height=5, width=50)
speech_text_box.pack()

translated_text_box = tk.Text(root, height=5, width=50)
translated_text_box.pack()

translate_button = tk.Button(root, text="Translate", command=process_speech)
translate_button.pack()

exit_button = tk.Button(root, text="Exit", command=handle_interrupt)
exit_button.pack()

# Initialize speech recognition and translation
r = sr.Recognizer()
translator = Translator()

try:
    # Run the GUI main loop
    root.mainloop()

except KeyboardInterrupt:
    print("Program stopped by keyboard interrupt.")
