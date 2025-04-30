import pyttsx3

def falar_resposta(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()
