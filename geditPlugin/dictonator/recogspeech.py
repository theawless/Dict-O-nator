#!/usr/bin/python3

import speech_recognition as sr
# Setting up logger
from dictonator.setlog import logger


class SpeechRecogniser2:
    # this is called from the background thread
    def __init__(self, f_bottom_bar_changer, f_plugin_bg_handler):
        # initialising this functions from the plugin
        self.bottom_bar_text_set = f_bottom_bar_changer
        self.plugin_bg_handler = f_plugin_bg_handler

        self.demand_fix_ambient_noise = True
        self.wants_to_run = False
        self.is_listening = False
        self.re = sr.Recognizer()
        self.mic = sr.Microphone()
        self.stop_listening = None
        self.source = None
        logger.debug("Speech Recogniser initialised")

    def start_recognising(self):
        while True:
            if self.wants_to_run:
                if self.is_listening:
                    if self.demand_fix_ambient_noise:
                        self.demand_fix_ambient_noise = False
                        self.bottom_bar_text_set("Preparing Dict'O'nator")
                        self.re.adjust_for_ambient_noise(self.source, 3)
                    self.bottom_bar_text_set("Speak now!")
                    time.sleep(0.1)
                else:
                    with self.mic as self.source:
                        self.demand_fix_ambient_noise = False
                        self.bottom_bar_text_set("Preparing Dict'O'nator")
                        self.re.adjust_for_ambient_noise(self.source, 3)
                    self.stop_listening = self.re.listen_in_background(self.mic, self.recog_callback)
                    self.is_listening = True
                    # stop_listening is now a function that, when called, stops background listening
            else:
                if self.is_listening:
                    self.bottom_bar_text_set("Stopping Dictation")
                    self.stop_listening()
                    self.bottom_bar_text_set("Stopped listening, to start listening press CTRL+ALT+2")
                    self.is_listening = False
                else:
                    time.sleep(0.1)

    def recog_callback(self, r, audio):
        settings = PluginSettings.settings
        sel = settings['Main']['recogniser']
        recognized_text = "######"
        # Recogniser begins
        if sel == "Sphinx":
            # Use Sphinx as recogniser
            self.bottom_bar_text_set("Got your words! Processing with Sphinx")
            logger.debug("recognize speech using Sphinx")
            try:
                recognized_text = r.recognize_sphinx(audio)
                logger.debug("From recogSpeech module: " + recognized_text)
            except sr.UnknownValueError:
                self.bottom_bar_text_set("Sphinx could not understand audio")
            except sr.RequestError as e:
                self.bottom_bar_text_set("Sphinx error; {0}".format(e))
            finally:
                self.plugin_bg_handler(recognized_text)

        elif sel == "Google":

            if settings['Google']['api_key'] != "":
                # Use Google with API KEY as recogniser
                GOOGLE_API_KEY = settings['Google']['api_key']
                self.bottom_bar_text_set("Got your words! Processing with Google Speech Recognition")
                logger.debug("recognize speech using Google Key Speech Recognition")
                try:
                    recognized_text = r.recognize_google(audio, GOOGLE_API_KEY)
                    logger.debug("From recogSpeech module G : " + recognized_text)
                except sr.UnknownValueError:
                    self.bottom_bar_text_set("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    self.bottom_bar_text_set(
                        "Could not request results from Google Speech Recognition service; {0}".format(e))
                finally:
                    self.plugin_bg_handler(recognized_text)
            else:
                self.bottom_bar_text_set("Got your words! Processing with Google Speech Recognition")
                logger.debug("recognize speech using Google Speech Recognition")
                try:
                    recognized_text = r.recognize_google(audio)
                    logger.debug("From recogSpeech module G : " + recognized_text)
                except sr.UnknownValueError:
                    self.bottom_bar_text_set("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    self.bottom_bar_text_set(
                        "Could not request results from Google Speech Recognition service; {0}".format(e))
                finally:
                    self.plugin_bg_handler(recognized_text)

        elif sel == "WITAI":
            # recognize speech using Wit.ai
            self.bottom_bar_text_set("Got your words! Processing with WIT.AI")
            logger.debug("recognize speech using WitAI Speech Recognition")

            WIT_AI_KEY = settings['WITAI']['api_key']
            # Wit.ai keys are 32-character uppercase alphanumeric strings
            try:
                recognized_text = r.recognize_wit(audio, key=WIT_AI_KEY)
                logger.debug("Wit.ai thinks you said " + recognized_text)
            except sr.UnknownValueError:
                self.bottom_bar_text_set("Wit.ai could not understand audio")
            except sr.RequestError as e:
                self.bottom_bar_text_set("Could not request results from Wit.ai service; {0}".format(e))
            finally:
                self.plugin_bg_handler(recognized_text)

        elif sel == "IBM":
            # recognize speech using IBM Speech to Text
            self.bottom_bar_text_set("Got your words! Processing with IBM")
            logger.debug("recognize speech using IBM Speech Recognition")

            IBM_USERNAME = settings['IBM']['username']
            # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
            IBM_PASSWORD = settings['IBM']['password']
            # IBM Speech to Text passwords are mixed-case alphanumeric strings
            try:
                recognized_text = r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)
                logger.debug("IBM Speech to Text thinks you said " + recognized_text)
            except sr.UnknownValueError:
                self.bottom_bar_text_set("IBM Speech to Text could not understand audio")
            except sr.RequestError as e:
                self.bottom_bar_text_set(
                    "Could not request results from IBM Speech to Text service; {0}".format(e))
            finally:
                self.plugin_bg_handler(recognized_text)

        elif sel == "ATT":
            # recognize speech using AT&T Speech to Text
            self.bottom_bar_text_set("Got your words! Processing with AT&T")
            logger.debug("recognize speech using AT&T Speech Recognition")

            ATT_APP_KEY = settings['ATT']['app_key']
            # AT&T Speech to Text app keys are 32-character lowercase alphanumeric strings
            ATT_APP_SECRET = settings['ATT']['app_secret']
            # AT&T Speech to Text app secrets are 32-character lowercase alphanumeric strings
            try:
                recognized_text = r.recognize_att(audio, app_key=ATT_APP_KEY, app_secret=ATT_APP_SECRET)
                logger.debug("AT&T Speech to Text thinks you said " + recognized_text)
            except sr.UnknownValueError:

                self.bottom_bar_text_set("AT&T Speech to Text could not understand audio")
            except sr.RequestError as e:
                self.bottom_bar_text_set(
                    "Could not request results from AT&T Speech to Text service; {0}".format(e))

            finally:
                self.plugin_bg_handler(recognized_text)


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
            try:
                self.r.adjust_for_ambient_noise(source, 2)
            except Exception as e:
                logger.debug(str(e))
                self.bottom_bar_text_set(str(e))

    def recog(self, settings):
        sel = settings['Main']['recogniser']
        logger.debug("Entered recog")
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
