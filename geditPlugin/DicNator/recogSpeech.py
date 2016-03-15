#!/usr/bin/python3

import speech_recognition as sr
# Setting up logger
import DicNator.setlog as setlog

logger = setlog.logger


class SpeechRecogniser:
    def __init__(self, f_bottom_bar_changer, p_is_thread_running):
        self.r = sr.Recognizer()
        # initialising this global function
        self.bottom_bar_text_set = f_bottom_bar_changer
        self.plugin_is_thread_running = p_is_thread_running
        logger.debug("Speech Recogniser initialised")

    def fix_ambient_noise(self):
        # Set threshold to ignore noises
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source, 3)

    def recog(self, settings):
        sel = settings['Main']['recogniser']
        # The main recognizer function that inputs audio and returns texts
        if not self.plugin_is_thread_running():
            # Check if the thread is running or it got cancelled
            return "######"
        # obtain audio from the microphone
        with sr.Microphone() as source:
            logger.debug("Say something!")

            audio = self.r.listen(source)
            # setting the default value of recognised text to something uncommon(impossible)
            recognized_text = "######"
            logger.debug("Got the audio!")
        if not self.plugin_is_thread_running():
            # Check if the thread is running or it got cancelled
            return "######"
        logger.debug(sel)
        # Recogniser begins
        if sel == "Sphinx":
            # Use Sphinx as recogniser
            self.bottom_bar_text_set("Got your words! Processing with Sphinx")
            logger.debug("recognize speech using Sphinx")
            try:
                recognized_text = self.r.recognize_sphinx(audio)
                logger.debug("From recogSpeech module S : " + recognized_text)
            except sr.UnknownValueError:
                self.bottom_bar_text_set("Sphinx could not understand audio")
            except sr.RequestError as e:
                self.bottom_bar_text_set("Sphinx error; {0}".format(e))
            finally:
                return recognized_text

        elif sel == "Google":

            if settings['Google']['api_key'] != "":
                # Use Google with API KEY as recogniser
                GOOGLE_API_KEY = settings['Google']['api_key']
                self.bottom_bar_text_set("Got your words! Processing with Google Speech Recognition")
                logger.debug("recognize speech using Google Key Speech Recognition")
                try:
                    recognized_text = self.r.recognize_google(audio, GOOGLE_API_KEY)
                    logger.debug("From recogSpeech module G : " + recognized_text)
                except sr.UnknownValueError:
                    self.bottom_bar_text_set("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    self.bottom_bar_text_set(
                        "Could not request results from Google Speech Recognition service; {0}".format(e))
                finally:
                    return recognized_text
            else:
                self.bottom_bar_text_set("Got your words! Processing with Google Speech Recognition")
                logger.debug("recognize speech using Google Speech Recognition")
                try:
                    recognized_text = self.r.recognize_google(audio)
                    logger.debug("From recogSpeech module G : " + recognized_text)
                except sr.UnknownValueError:
                    self.bottom_bar_text_set("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    self.bottom_bar_text_set(
                        "Could not request results from Google Speech Recognition service; {0}".format(e))
                finally:
                    return recognized_text

        elif sel == "WITAI":
            # recognize speech using Wit.ai
            self.bottom_bar_text_set("Got your words! Processing with WIT.AI")
            logger.debug("recognize speech using WitAI Speech Recognition")

            WIT_AI_KEY = settings['WITAI']['api_key']
            # Wit.ai keys are 32-character uppercase alphanumeric strings
            try:
                recognized_text = self.r.recognize_wit(audio, key=WIT_AI_KEY)
                logger.debug("Wit.ai thinks you said " + recognized_text)
            except sr.UnknownValueError:
                self.bottom_bar_text_set("Wit.ai could not understand audio")
            except sr.RequestError as e:
                self.bottom_bar_text_set("Could not request results from Wit.ai service; {0}".format(e))
            finally:
                return recognized_text

        elif sel == "IBM":
            # recognize speech using IBM Speech to Text
            self.bottom_bar_text_set("Got your words! Processing with IBM")
            logger.debug("recognize speech using IBM Speech Recognition")

            IBM_USERNAME = settings['IBM']['username']
            # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
            IBM_PASSWORD = settings['IBM']['password']
            # IBM Speech to Text passwords are mixed-case alphanumeric strings
            try:
                recognized_text = self.r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)
                logger.debug("IBM Speech to Text thinks you said " + recognized_text)
            except sr.UnknownValueError:
                self.bottom_bar_text_set("IBM Speech to Text could not understand audio")
            except sr.RequestError as e:
                self.bottom_bar_text_set("Could not request results from IBM Speech to Text service; {0}".format(e))
            finally:
                return recognized_text

        elif sel == "ATT":
            # recognize speech using AT&T Speech to Text
            self.bottom_bar_text_set("Got your words! Processing with AT&T")
            logger.debug("recognize speech using AT&T Speech Recognition")

            ATT_APP_KEY = settings['ATT']['app_key']
            # AT&T Speech to Text app keys are 32-character lowercase alphanumeric strings
            ATT_APP_SECRET = settings['ATT']['app_secret']
            # AT&T Speech to Text app secrets are 32-character lowercase alphanumeric strings
            try:
                recognized_text = self.r.recognize_att(audio, app_key=ATT_APP_KEY, app_secret=ATT_APP_SECRET)
                logger.debug("AT&T Speech to Text thinks you said " + recognized_text)
            except sr.UnknownValueError:

                self.bottom_bar_text_set("AT&T Speech to Text could not understand audio")
            except sr.RequestError as e:
                self.bottom_bar_text_set("Could not request results from AT&T Speech to Text service; {0}".format(e))

            finally:
                return recognized_text
