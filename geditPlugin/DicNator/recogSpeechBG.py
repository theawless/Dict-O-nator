import speech_recognition as sr
import DicNator.setlog

# setting up logger
logger = DicNator.setlog.logger


def bottom_bar_text_set(txt):
    pass


# this is called from the background thread
def callback(r, audio, settings):
    sel = settings['Main']['recogniser']
    logger.debug(sel)

    # Recogniser begins
    if sel == "Sphinx":
        # Use Sphinx as recogniser
        bottom_bar_text_set("Got your words! Processing with Sphinx")
        logger.debug("recognize speech using Sphinx")
        try:
            recognized_text = r.recognize_sphinx(audio)
            logger.debug("From recogSpeech module S : " + recognized_text)
        except sr.UnknownValueError:
            bottom_bar_text_set("Sphinx could not understand audio")
        except sr.RequestError as e:
            bottom_bar_text_set("Sphinx error; {0}".format(e))
        finally:
            return recognized_text

    elif sel == "Google":

        if settings['Google']['api_key'] != "":
            # Use Google with API KEY as recogniser
            GOOGLE_API_KEY = settings['Google']['api_key']
            bottom_bar_text_set("Got your words! Processing with Google Speech Recognition")
            logger.debug("recognize speech using Google Key Speech Recognition")
            try:
                recognized_text = r.recognize_google(audio, GOOGLE_API_KEY)
                logger.debug("From recogSpeech module G : " + recognized_text)
            except sr.UnknownValueError:
                bottom_bar_text_set("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                bottom_bar_text_set(
                    "Could not request results from Google Speech Recognition service; {0}".format(e))
            finally:
                return recognized_text
        else:
            bottom_bar_text_set("Got your words! Processing with Google Speech Recognition")
            logger.debug("recognize speech using Google Speech Recognition")
            try:
                recognized_text = r.recognize_google(audio)
                logger.debug("From recogSpeech module G : " + recognized_text)
            except sr.UnknownValueError:
                bottom_bar_text_set("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                bottom_bar_text_set(
                    "Could not request results from Google Speech Recognition service; {0}".format(e))
            finally:
                return recognized_text

    elif sel == "WITAI":
        # recognize speech using Wit.ai
        bottom_bar_text_set("Got your words! Processing with WIT.AI")
        logger.debug("recognize speech using WitAI Speech Recognition")

        WIT_AI_KEY = settings['WITAI']['api_key']
        # Wit.ai keys are 32-character uppercase alphanumeric strings
        try:
            recognized_text = r.recognize_wit(audio, key=WIT_AI_KEY)
            logger.debug("Wit.ai thinks you said " + recognized_text)
        except sr.UnknownValueError:
            bottom_bar_text_set("Wit.ai could not understand audio")
        except sr.RequestError as e:
            bottom_bar_text_set("Could not request results from Wit.ai service; {0}".format(e))
        finally:
            return recognized_text

    elif sel == "IBM":
        # recognize speech using IBM Speech to Text
        bottom_bar_text_set("Got your words! Processing with IBM")
        logger.debug("recognize speech using IBM Speech Recognition")

        IBM_USERNAME = settings['IBM']['username']
        # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
        IBM_PASSWORD = settings['IBM']['password']
        # IBM Speech to Text passwords are mixed-case alphanumeric strings
        try:
            recognized_text = r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)
            logger.debug("IBM Speech to Text thinks you said " + recognized_text)
        except sr.UnknownValueError:
            bottom_bar_text_set("IBM Speech to Text could not understand audio")
        except sr.RequestError as e:
            bottom_bar_text_set("Could not request results from IBM Speech to Text service; {0}".format(e))
        finally:
            return recognized_text

    elif sel == "ATT":
        # recognize speech using AT&T Speech to Text
        bottom_bar_text_set("Got your words! Processing with AT&T")
        logger.debug("recognize speech using AT&T Speech Recognition")

        ATT_APP_KEY = settings['ATT']['app_key']
        # AT&T Speech to Text app keys are 32-character lowercase alphanumeric strings
        ATT_APP_SECRET = settings['ATT']['app_secret']
        # AT&T Speech to Text app secrets are 32-character lowercase alphanumeric strings
        try:
            recognized_text = r.recognize_att(audio, app_key=ATT_APP_KEY, app_secret=ATT_APP_SECRET)
            logger.debug("AT&T Speech to Text thinks you said " + recognized_text)
        except sr.UnknownValueError:

            bottom_bar_text_set("AT&T Speech to Text could not understand audio")
        except sr.RequestError as e:
            bottom_bar_text_set("Could not request results from AT&T Speech to Text service; {0}".format(e))

        finally:
            return recognized_text


re = sr.Recognizer()
m = sr.Microphone()
with m as source:
    re.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = re.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# do some other computation for 5 seconds, then stop listening and keep doing other computations
import time

for _ in range(50):
    time.sleep(0.1)  # we're still listening even though the main thread is doing other things
stop_listening()  # calling this function requests that the background listener stop listening
while True:
    time.sleep(0.1)
