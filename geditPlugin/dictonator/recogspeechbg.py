import speech_recognition as sr
from .setlog import logger
import time
from .configurablesettings import PluginSettings
from gi.repository import GLib


class SpeechRecogniser:
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
                        GLib.idle_add(self.bottom_bar_text_set, "Preparing Dict'O'nator")
                        self.re.adjust_for_ambient_noise(self.source, 3)
                    GLib.idle_add(self.bottom_bar_text_set, "Speak now!")
                    time.sleep(0.1)
                else:
                    with self.mic as self.source:
                        self.demand_fix_ambient_noise = False
                        GLib.idle_add(self.bottom_bar_text_set, "Preparing Dict'O'nator")
                        self.re.adjust_for_ambient_noise(self.source, 3)
                    self.stop_listening = self.re.listen_in_background(self.mic, self.recog_callback)
                    self.is_listening = True
                    # stop_listening is now a function that, when called, stops background listening
            else:
                if self.is_listening:
                    GLib.idle_add(self.bottom_bar_text_set, "Stopping Dictation")
                    self.stop_listening()
                    GLib.idle_add(self.bottom_bar_text_set, "Stopped listening, to start listening press CTRL+ALT+2")
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
                GLib.idle_add(self.bottom_bar_text_set, "Sphinx could not understand audio")
            except sr.RequestError as e:
                GLib.idle_add(self.bottom_bar_text_set, "Sphinx error; {0}".format(e))
            finally:
                GLib.idle_add(self.plugin_bg_handler, recognized_text)

        elif sel == "Google":

            if settings['Google']['api_key'] != "":
                # Use Google with API KEY as recogniser
                GOOGLE_API_KEY = settings['Google']['api_key']
                GLib.idle_add(self.bottom_bar_text_set, "Got your words! Processing with Google Speech Recognition")
                logger.debug("recognize speech using Google Key Speech Recognition")
                try:
                    recognized_text = r.recognize_google(audio, GOOGLE_API_KEY)
                    logger.debug("From recogSpeech module G : " + recognized_text)
                except sr.UnknownValueError:
                    GLib.idle_add(self.bottom_bar_text_set, "Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    GLib.idle_add(self.bottom_bar_text_set,
                                  "Could not request results from Google Speech Recognition service; {0}".format(e))
                finally:
                    GLib.idle_add(self.plugin_bg_handler, recognized_text)
            else:
                GLib.idle_add(self.bottom_bar_text_set, "Got your words! Processing with Google Speech Recognition")
                logger.debug("recognize speech using Google Speech Recognition")
                try:
                    recognized_text = r.recognize_google(audio)
                    logger.debug("From recogSpeech module G : " + recognized_text)
                except sr.UnknownValueError:
                    GLib.idle_add(self.bottom_bar_text_set, "Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    GLib.idle_add(self.bottom_bar_text_set,
                                  "Could not request results from Google Speech Recognition service; {0}".format(e))
                finally:
                    GLib.idle_add(self.plugin_bg_handler, recognized_text)

        elif sel == "WITAI":
            # recognize speech using Wit.ai
            GLib.idle_add(self.bottom_bar_text_set, "Got your words! Processing with WIT.AI")
            logger.debug("recognize speech using WitAI Speech Recognition")

            WIT_AI_KEY = settings['WITAI']['api_key']
            # Wit.ai keys are 32-character uppercase alphanumeric strings
            try:
                recognized_text = r.recognize_wit(audio, key=WIT_AI_KEY)
                logger.debug("Wit.ai thinks you said " + recognized_text)
            except sr.UnknownValueError:
                GLib.idle_add(self.bottom_bar_text_set, "Wit.ai could not understand audio")
            except sr.RequestError as e:
                GLib.idle_add(self.bottom_bar_text_set, "Could not request results from Wit.ai service; {0}".format(e))
            finally:
                GLib.idle_add(self.plugin_bg_handler, recognized_text)

        elif sel == "IBM":
            # recognize speech using IBM Speech to Text
            GLib.idle_add(self.bottom_bar_text_set, "Got your words! Processing with IBM")
            logger.debug("recognize speech using IBM Speech Recognition")

            IBM_USERNAME = settings['IBM']['username']
            # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
            IBM_PASSWORD = settings['IBM']['password']
            # IBM Speech to Text passwords are mixed-case alphanumeric strings
            try:
                recognized_text = r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)
                logger.debug("IBM Speech to Text thinks you said " + recognized_text)
            except sr.UnknownValueError:
                GLib.idle_add(self.bottom_bar_text_set, "IBM Speech to Text could not understand audio")
            except sr.RequestError as e:
                GLib.idle_add(self.bottom_bar_text_set,
                              "Could not request results from IBM Speech to Text service; {0}".format(e))
            finally:
                GLib.idle_add(self.plugin_bg_handler, recognized_text)

        elif sel == "ATT":
            # recognize speech using AT&T Speech to Text
            GLib.idle_add(self.bottom_bar_text_set, "Got your words! Processing with AT&T")
            logger.debug("recognize speech using AT&T Speech Recognition")

            ATT_APP_KEY = settings['ATT']['app_key']
            # AT&T Speech to Text app keys are 32-character lowercase alphanumeric strings
            ATT_APP_SECRET = settings['ATT']['app_secret']
            # AT&T Speech to Text app secrets are 32-character lowercase alphanumeric strings
            try:
                recognized_text = r.recognize_att(audio, app_key=ATT_APP_KEY, app_secret=ATT_APP_SECRET)
                logger.debug("AT&T Speech to Text thinks you said " + recognized_text)
            except sr.UnknownValueError:

                GLib.idle_add(self.bottom_bar_text_set, "AT&T Speech to Text could not understand audio")
            except sr.RequestError as e:
                GLib.idle_add(self.bottom_bar_text_set,
                              "Could not request results from AT&T Speech to Text service; {0}".format(e))

            finally:
                GLib.idle_add(self.plugin_bg_handler, recognized_text)
