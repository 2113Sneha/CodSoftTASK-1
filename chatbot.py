import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

# Use the first voice (male voice in Windows)
engine.setProperty('voice', voices[0].id)

def speak(audio):
    """Converts text to speech"""
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """Greets the user according to the current time"""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am KOOGlE. Please tell me how may I help you")

def takeCommand():
    """Takes microphone input from the user and returns a string output"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1  # Time to pause before considering the end of a sentence
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')  # Recognizes English (India)
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def sendEmail(to, content):
    """Sends an email using SMTP protocol"""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        # Log in to your email using App Password
        server.login('youremail@gmail.com', 'your-app-password')
        server.sendmail('youremail@gmail.com', to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("Sorry, I am not able to send the email.")

def executeTask(query):
    """Executes a task based on the query"""
    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    elif 'open youtube' in query:
        webbrowser.open("https://youtube.com")

    elif 'open google' in query:
        webbrowser.open("https://google.com")

    elif 'open stackoverflow' in query:
        webbrowser.open("https://stackoverflow.com")

    elif 'play music' in query:
        # Replace with the path to your music directory on Windows
        music_dir = 'D:\\songs'
        songs = os.listdir(music_dir)
        print(songs)
        os.startfile(os.path.join(music_dir, songs[0]))

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")

    elif 'open code' in query:
        # Replace with the path to your VS Code installation on Windows
        codePath = "C:\\Users\\YourUser\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(codePath)

    elif 'email to harry' in query:
        try:
            speak("What should I say?")
            content = takeCommand()
            to = "harryyourEmail@gmail.com"  # Replace with recipient email
            sendEmail(to, content)
        except Exception as e:
            print(e)
            speak("Sorry, I am not able to send this email.")

if __name__ == "__main__":
    wishMe()

    # Initialize count for commands executed
    command_count = 0

    # Continue executing commands until at least two tasks are done
    while command_count < 2:
        query = takeCommand().lower()

        # If the user wants to quit early, break the loop
        if 'quit' in query:
            speak("Goodbye!")
            break

        # Check if the recognized command can be executed
        if query != "None":
            executeTask(query)
            command_count += 1

            if command_count < 2:
                speak("What else can I do for you?")
            else:
                speak("I have completed two tasks. Would you like to perform more tasks? Say yes or no.")
                next_command = takeCommand().lower()
                if 'yes' in next_command:
                    command_count = 0  # Reset the count for a new round of tasks
                elif 'no' in next_command or 'quit' in next_command:
                    speak("Goodbye!")
                    break
                else:
                    speak("I will continue to assist you.")
