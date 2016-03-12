#!/usr/bin/python3

import speech_recognition as sr
# Setting up logger
import setlog

logger = setlog.logger


class SpeechRecogniser:
    def __init__(self):
        self.r = sr.Recognizer()

    def fix_ambient_noise(self):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source, 3)

    def recog(self, sel="Sphinx"):
        # The main recognizer function that inputs audio and returns texts
        # obtain audio from the microphone
        with sr.Microphone() as source:
            logger.debug("Say something!")

            audio = r.listen(source)
            recognized_text = ""
            logger.debug("Got it!")
        if sel == "Sphinx":
            logger.debug("recognize speech using Sphinx")
            try:
                recognized_text = r.recognize_sphinx(audio)
                logger.debug("From recogSpeech module S : " + recognized_text)
            except sr.UnknownValueError:
                logger.debug("Sphinx could not understand audio")
            except sr.RequestError as e:
                logger.debug("Sphinx error; {0}".format(e))
            finally:
                return recognized_text
        elif sel == "Google":
            logger.debug("recognize speech using Google Speech Recognition")
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                recognized_text = r.recognize_google(audio)
                logger.debug("From recogSpeech module G : " + recognized_text)
            except sr.UnknownValueError:
                logger.debug("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                logger.debug("Could not request results from Google Speech Recognition service; {0}".format(e))
            finally:
                return recognized_text
