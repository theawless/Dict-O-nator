#!/usr/bin/python3

import speech_recognition as sr
# Setting up logger
import setlog
logger=setlog.logger
def recog():
    # The main recognizer function that inputs audio and returns texts

    r = sr.Recognizer()
    # obtain audio from the microphone    
    with sr.Microphone() as source:
        logger.debug("Say something!")
        audio = r.listen(source)
    # recognize speech using Sphinx
    try:
        recognized_text=""
        recognized_text=r.recognize_sphinx(audio)
        logger.debug("From recogSpeech module: "+recognized_text)
    except sr.UnknownValueError:
        logger.debug("Sphinx could not understand audio")
    except sr.RequestError as e:
        logger.debug("Sphinx error; {0}".format(e))    
    finally:
        return recognized_text

    # recognize speech using Google Speech Recognition    
    '''
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    '''
