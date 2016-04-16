from .test_pluginSettings import TestPluginSettings
from .test_speechRecogniser import TestSpeechRecogniser


class AllTestSuite:
    def __init__(self):
        self.test_settings = TestPluginSettings()
        self.test_stt = TestSpeechRecogniser()

    def run_all_tests(self):
        self.test_settings.setUp()
        self.test_settings.run()
        print("Settings test finished")
        self.test_stt.setUp()
        self.test_stt.run()
        print("All tests finished")


a = AllTestSuite()
a.run_all_tests()
