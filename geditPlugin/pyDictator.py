#!/usr/bin/python3

import sys
sys.path.append('.local/share/gedit/plugins/')
import setlog
import recogSpeech
import threading

import statesMod
# Getting the states
states=statesMod.states
# Setting up logger
logger=setlog.logger
logger.debug('Start Plugin')

from gi.repository import GObject, Gtk, Gedit
# Defining the UI string that is to be added
ui_str = """
<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_2">
        <menu name="DicNator" action="DicNator">
          <menuitem name="Clear" action="Clear"/>
          <menuitem name="Listen" action="Listen"/>
          <menuitem name="Stop" action="Stop"/>
        </menu>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

class backgroundThread (threading.Thread):
    def __init__(self,instance):
        threading.Thread.__init__(self)
        self.pluginClass=instance
    def run(self):
        logger.debug(self.name+" run thread")
        self.pluginClass.bgCallHandler()
    def stop(self):
        logger.debug(self.name+" stop thread")
        
class DicNatorPlugin(GObject.Object,Gedit.WindowActivatable):
    __gtype_name__= "DicNator"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self):
        # Constructor
        GObject.Object.__init__(self)
        self.thread_isRunning=False
        self.thread=backgroundThread(self)
        logger.debug('Init end')

    def do_activate(self):
        # Insert menu to gui
        self._insert_menu()
        logger.debug("Finished inserting menu")

    def do_deactivate(self):
        # Remove any installed menu items
        self._remove_menu()
        self._action_group = None
        logger.debug("Finished removing menu")
        
    def _insert_menu(self):
        actions = [
            ('DicNator',None,'DicNator'),
            ("Clear", None, "Clear document",'<Control><Alt>1', "Clear the document",self.on_clear_document_activate),
            ("Listen", None, "Start Listening",'<Control><Alt>2', "Start Listening",self.on_listen_activate),
            ("Stop", None, "Stop Listening",'<Control><Alt>3', "Stop Listening",self.on_stop_activate)
        ]
        
        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()
        # Create a new action group
        self._action_group = Gtk.ActionGroup("DicNatorPluginActions")
        self._action_group.add_actions(actions)
        # Insert the action group
        manager.insert_action_group(self._action_group)
        # Merge the UI
        self._ui_id = manager.add_ui_from_string(ui_str)        
                
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
    
    def on_clear_document_activate(self, action):
        # Clears the document
        logger.debug("cleared the doc")
        doc = self.window.get_active_document()
        if not doc:
            return
        doc.set_text('')

    def on_listen_activate(self, action):
        # For debugging purposes we will start dictator on call only
        self.do_log('Thread Started')
        # Calling the background handler in a different thread
        self.thread_isRunning=True
        self.thread.start()

    def on_stop_activate(self, action):
        # For debugging purposes we will stop dictator on call only
        self.do_log('Thread Stopping')
        #Stopping the background handler
        self.thread_isRunning=False
        self.thread.stop()
        self.do_log('Stopped')

    def insertText(self,text="Default insertText"):
        # Inserts the text in the document
        doc = self.window.get_active_document()
        doc.begin_user_action()
        doc.insert_at_cursor(text)
        doc.end_user_action()

    def _callRecog(self):
        # Calls recognizer and gets the text output
        textOut=recogSpeech.recog(1)
        _state=statesMod.decideState(textOut)
        return (textOut,_state)

    def bgCallHandler(self):
        # Based on output by the callRecog we proceed further
        logger.debug("Inside bgcallhandler")
        if self.thread_isRunning==False:
            logger.debug("Thread not running")
            return
        (text,currState)=self._callRecog()
        if currState==states[0]:
            self.insertText(text)
            self.bgCallHandler()
        else:
            logger.debug("End Background Call Handler")
            return
