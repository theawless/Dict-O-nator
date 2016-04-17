# Dict'O'nator - A dictation plugin for gedit.
# Copyright (C) <2016>  <Abhinav Singh>
#
# This file is part of Dict'O'nator.
#
# Dict'O'nator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Dict'O'nator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Dict'O'nator.  If not, see <http://www.gnu.org/licenses/>.


import speech_recognition as sr
from gi.repository import GLib, Gtk

from .configurablesettings import PluginSettings
from .setlog import logger


class SpeechRecogniser:
    """Voice recogniser class."""

    # this is called from the background thread
    def __init__(self, f_bottom_bar_changer: callable, f_action_handler: callable):
        """Constructor.

        :param f_bottom_bar_changer: change the bottom bar main text.
        :param f_action_handler: do action based on received text.
        """
        self.bottom_bar_text_set = f_bottom_bar_changer
        self.plugin_action_handler = f_action_handler
        self.source = None
        self.re = sr.Recognizer()
        self.mic = sr.Microphone()
        self.re_stopper = None
        self.is_listening = False
        self.is_prepared = False
        logger.debug("Speech Recogniser initialised")

    @staticmethod
    def update_gui():
        """Updates GUI by completing all tasks in the main event loop"""
        while Gtk.events_pending():
            Gtk.main_iteration_do(True)

    def start_recognising(self):
        """Start listening to voice."""
        if not self.is_prepared:
            self.setup_recogniser()
        if not self.is_listening:
            self.re_stopper = self.re.listen_in_background(self.mic, self.recog_callback)
            self.is_listening = True
            self.bottom_bar_text_set("Speak!")
        else:
            self.stop_recognising()
            self.start_recognising()

    def setup_recogniser(self):
        """Adjusts for noise."""
        self.bottom_bar_text_set("Preparing Dict'O'nator...")
        self.update_gui()
        if self.is_listening:
            self.re.adjust_for_ambient_noise(self.source, duration=2)
        else:
            with self.mic as source:
                self.source = source
                self.re.adjust_for_ambient_noise(source, duration=2)
        self.is_prepared = True
        self.bottom_bar_text_set("Done preparing.")

    def stop_recognising(self):
        """Stops listening."""
        if self.is_listening:
            self.bottom_bar_text_set("Stopping Dictation!")
            self.update_gui()
            self.re_stopper()
            self.is_listening = False
            self.bottom_bar_text_set("Stopped listening, to start listening press CTRL+ALT+2")
        else:
            self.bottom_bar_text_set("Dictation is already OFF")

    def recog_callback(self, r, audio, testing=False):
        """
        Called from different thread. Uses GLib.idle_all to add function to main loop.
        Callback for start_recogniser, converts speech to text.
        Calls action_handler in main thread.
        """
        settings = PluginSettings.settings
        sel = settings['Main']['recogniser']
        recognized_text = "######"
        # Recogniser begins
        if sel == "Sphinx":
            # Use Sphinx as recogniser
            GLib.idle_add(self.bottom_bar_text_set, "Got your words! Processing with Sphinx")
            logger.debug("recognize speech using Sphinx")
            try:
                recognized_text = r.recognize_sphinx(audio)
                logger.debug("From recogSpeech module: " + recognized_text)
            except sr.UnknownValueError:
                GLib.idle_add(self.bottom_bar_text_set, "Sphinx could not understand audio")
            except sr.RequestError as e:
                GLib.idle_add(self.bottom_bar_text_set, "Sphinx error; {0}".format(e))
            finally:
                GLib.idle_add(self.plugin_action_handler, recognized_text)
                if testing:
                    self.plugin_action_handler(recognized_text)
        elif sel == "Google":

            if settings['Google']['api_key'] != "":
                # Use Google with API KEY as recogniser
                google_api_key = settings['Google']['api_key']
                GLib.idle_add(self.bottom_bar_text_set, "Got your words! Processing with Google Speech Recognition")
                logger.debug("recognize speech using Google Key Speech Recognition")
                try:
                    recognized_text = r.recognize_google(audio, google_api_key)
                    logger.debug("From recogSpeech module G : " + recognized_text)
                except sr.UnknownValueError:
                    GLib.idle_add(self.bottom_bar_text_set, "Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    GLib.idle_add(self.bottom_bar_text_set,
                                  "Could not request results from Google Speech Recognition service; {0}".format(e))
                finally:
                    GLib.idle_add(self.plugin_action_handler, recognized_text)
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
                    GLib.idle_add(self.plugin_action_handler, recognized_text)

        elif sel == "WITAI":
            # recognize speech using Wit.ai
            GLib.idle_add(self.bottom_bar_text_set, "Got your words! Processing with WIT.AI")
            logger.debug("recognize speech using WitAI Speech Recognition")

            wit_ai_key = settings['WITAI']['api_key']
            # Wit.ai keys are 32-character uppercase alphanumeric strings
            try:
                recognized_text = r.recognize_wit(audio, key=wit_ai_key)
                logger.debug("Wit.ai thinks you said " + recognized_text)
            except sr.UnknownValueError:
                GLib.idle_add(self.bottom_bar_text_set, "Wit.ai could not understand audio")
            except sr.RequestError as e:
                GLib.idle_add(self.bottom_bar_text_set, "Could not request results from Wit.ai service; {0}".format(e))
            finally:
                GLib.idle_add(self.plugin_action_handler, recognized_text)

        elif sel == "Bing":
            # recognize speech using Microsoft Bing Voice Recognition
            GLib.idle_add(self.bottom_bar_text_set, "Got your words! Processing with Bing")
            logger.debug("recognize speech using Bing Speech Recognition")

            bing_key = settings['Bing']['api_key']
            try:
                recognized_text = r.recognize_bing(audio, key=bing_key)
                logger.debug("Microsoft Bing Voice Recognition thinks you said " + recognized_text)
            except sr.UnknownValueError:
                GLib.idle_add(self.bottom_bar_text_set, "Microsoft Bing Voice Recognition could not understand audio")
            except sr.RequestError as e:
                GLib.idle_add(self.bottom_bar_text_set,
                              "Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
            finally:
                GLib.idle_add(self.plugin_action_handler, recognized_text)

        elif sel == "APIAI":
            # recognize speech using api.ai
            GLib.idle_add(self.bottom_bar_text_set, "Got your words! Processing with API.AI")
            logger.debug("recognize speech using APIAI Speech Recognition")

            api_ai_client_access_token = settings['APIAI']['api_key']
            try:
                recognized_text = r.recognize_api(audio, client_access_token=api_ai_client_access_token)
                logger.debug("api.ai thinks you said " + recognized_text)
            except sr.UnknownValueError:
                GLib.idle_add(self.bottom_bar_text_set, "api.ai could not understand audio")
            except sr.RequestError as e:
                GLib.idle_add(self.bottom_bar_text_set, "Could not request results from api.ai service; {0}".format(e))
            finally:
                GLib.idle_add(self.plugin_action_handler, recognized_text)

        elif sel == "IBM":
            # recognize speech using IBM Speech to Text
            GLib.idle_add(self.bottom_bar_text_set, "Got your words! Processing with IBM")
            logger.debug("recognize speech using IBM Speech Recognition")

            ibm_username = settings['IBM']['username']
            # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
            ibm_password = settings['IBM']['password']
            # IBM Speech to Text passwords are mixed-case alphanumeric strings
            try:
                recognized_text = r.recognize_ibm(audio, username=ibm_username, password=ibm_password)
                logger.debug("IBM Speech to Text thinks you said " + recognized_text)
            except sr.UnknownValueError:
                GLib.idle_add(self.bottom_bar_text_set, "IBM Speech to Text could not understand audio")
            except sr.RequestError as e:
                GLib.idle_add(self.bottom_bar_text_set,
                              "Could not request results from IBM Speech to Text service; {0}".format(e))
            finally:
                GLib.idle_add(self.plugin_action_handler, recognized_text)
