from time import strftime
import speech_recognition as sr
import re
import webbrowser
import pyttsx3
import wikipedia
import requests


def jarvis(audio):
    print(audio)
    engine = pyttsx3.init()
    engine.say(audio)
    engine.runAndWait()

#myCommand is used 
def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say...")
        r.pause_threshold = 0.8
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print("You said:" + command + '\n')
    except sr.UnknownValueError:
        print("...")
        command = myCommand()
    return command


def assistant(command):
    command = command.lower()
    # open youtube
    if 'open youtube' in command:
        reg_ex = re.search('open youtube (.*)', command)

        url = "https://www.youtube.com/"
        if reg_ex:
            yt = reg_ex.group(1)
            url = url + 'r/' + sub_yt
        webbrowser.open(url)
        jarvis("The youtube content is opened to you")
    # shuting down the assistant
    elif 'shutdown' in command:
        jarvis("Bye bye Sir. Have a nice day.")
        exit(-1)
    #tell me about
    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                jarvis(ny.content[:500].encode('utf-8'))
        except Exception as e:
            print(e)
            jarvis(e)
    # tell me a joke
    elif 'joke' in command:
        res = requests.get(
            'https://icanhazdadjoke.com/',
            headers={"Accept": "application/json"})
        if res.status_code == requests.codes.ok:
            print(res.json())
            jarvis(str(res.json()['joke']))
        else:
            jarvis('oops!I ran out of jokes')
    # time
    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        jarvis('Current time is %d hours %d minutes' % (now.hour, now.minute))
    # greetings
    elif 'hello' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            jarvis('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            jarvis('Hello Sir. Good afternoon')
        else:
            jarvis('Hello Sir. Good evening')
    #help me
    elif 'help me' in command:
        jarvis("""
            You can use these commands and I'll help you out:
    1. Open youtube : Opens the youtube in default browser.
            2. Open xyz.com : replace xyz with any website name
            3. Hello
            4. news for today : reads top news of today
            5. tell me a joke
            6. tell me about xyz : tells you about xyz
            7. time : Current system time
            """)
    # open website
    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain + '.com/'
            webbrowser.open(url)
            jarvis('The website you have requested has been opened for you Sir.')
        else:
            jarvis("Sir, kindly tell us the topic")


jarvis('Hi User, I am jarvis and I am your personal voice assistant, Please give a command or say "help me" and '
       'I will tell you what all I can do for you.')

while True:
    assistant(myCommand())
