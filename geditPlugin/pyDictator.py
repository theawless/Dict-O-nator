#!/usr/bin/python3
import sys
sys.path.append('.local/share/gedit/plugins/')
import setlog
logger=setlog.logger
logger.debug('Start Plugin')
import speech_recognition as sr
import threading
import time
from gi.repository import GObject, Gtk, Gedit
ui_str = """
<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_2">
        <menu name="PyDictator" action="PyDictator">
          <menuitem name="Clear" action="Clear"/>
          <menuitem name="Logit" action="Logit"/>
        </menu>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

class PyDictatorPlugin(GObject.Object,Gedit.WindowActivatable):
    __gtype_name__= "PyDictator"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)
        logger.debug('Init end')

    def do_activate(self):
        # Insert menu items
        self._insert_menu()
        logger.debug("Finished inserting menu")

    def do_deactivate(self):
        # Remove any installed menu items
        self._remove_menu()
        self._action_group = None
        logger.debug("Finished inserting menu")
        
    def _insert_menu(self):
        actions = [
            ('PyDictator',None,'PyDictator'),
            ("Clear", None, "Clear document",'<Control><Alt>1', "Clear the document",self.on_clear_document_activate),
            ("Logit", None, "Log now",'<Control><Alt>2', "Log now ",self.on_logit_activate)
        ]
        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()
        # Create a new action group
        self._action_group = Gtk.ActionGroup("PyDictatorPluginActions")
        self._action_group.add_actions(actions)
        # Insert the action group
        manager.insert_action_group(self._action_group)
        # Merge the UI
        self._ui_id = manager.add_ui_from_string(ui_str)        
        
        #oldmethod        
        #self._ui_merge_id = manager.add_ui_from_string(ui_str)
        #manager.ensure_update()
        
    def _remove_menu(self):
        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()

        # Remove the ui
        manager.remove_ui(self._ui_id)

        # Remove the action group
        manager.remove_action_group(self._action_group)

        # Make sure the manager updates
        manager.ensure_update()
    
    def do_log(self, msg='Default do_log Message'):
        logger.debug(msg)
    
    def do_update_state(self):
        self._action_group.set_sensitive(self.window.get_active_document() != None)

    # Menu activate handlers
    def on_clear_document_activate(self, action):
        doc = self.window.get_active_document()
        if not doc:
            return
        doc.set_text('')

    def on_logit_activate(self, action):
        self.do_log('Executing my action')
        #self.some_func()
        thread=threading.Thread(target=self.always, args=())
        thread.daemon=True;
        thread.start()
        
    def always(self):
        while True:
            self.do_log("Debug Infinite Background Function")

    def callback(recognizer, audio):
        # received audio data, now we'll recognize it using Google Speech Recognition
        logger.debug("In Callback function")
        try:
            text_out=recognizer.recognize_sphinx(audio)
            print("Sphinx Speech Recognition thinks you said " +text_out )
            if text_out=='hello':
                logger.debug('something')
        except sr.UnknownValueError:
            print("Sphinx Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Sphinx Speech Recognition service; {0}".format(e))
    
    def recognize_(self):
        r = sr.Recognizer()
        m = sr.Microphone()
        with m as source:
            r.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening
        # start listening in the background (note that we don't have to do this inside a `with` statement)
        stop_listening = r.listen_in_background(m, self.callback)
        # `stop_listening` is now a function that, when called, stops background listening

        # do some other computation for 5 seconds, then stop listening and keep doing other computations
        for _ in range(5): time.sleep(0.1) # we're still listening even though the main thread is doing other things
        stop_listening() # calling this function requests that the background listener stop listening
        while True: time.sleep(0.1)

