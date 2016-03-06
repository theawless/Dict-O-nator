#!/usr/bin/python3

import speech_recognition as sr
# Setting up logger
import setlog
logger=setlog.logger
def recog(sel=0):
    # The main recognizer function that inputs audio and returns texts
    r = sr.Recognizer()
    # obtain audio from the microphone    
    with sr.Microphone() as source:
        logger.debug("Say something!")
        try:        
            audio = r.listen(source)
        except:
            logger.debug("some error in listening")        
        recognized_text=""
        logger.debug("Got it!")
    if sel==0:
        logger.debug("recognize speech using Sphinx")
        try:
            recognized_text=r.recognize_sphinx(audio)
            logger.debug("From recogSpeech module S : "+recognized_text)
        except sr.UnknownValueError:
            logger.debug("Sphinx could not understand audio")
        except sr.RequestError as e:
            logger.debug("Sphinx error; {0}".format(e))    
        finally:
            return recognized_text
    elif sel==1:
        logger.debug("recognize speech using Google Speech Recognition")    
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            recognized_text=r.recognize_google(audio)
            logger.debug("From recogSpeech module G : "+recognized_text)
        except sr.UnknownValueError:
            logger.debug("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            logger.debug("Could not request results from Google Speech Recognition service; {0}".format(e))
        finally:
            return recognized_text
