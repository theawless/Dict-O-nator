#!/usr/bin/python3

from gi.repository import GObject, Gtk, Gedit, PeasGtk
from .setlog import logger
from .configurablesettings import ConfigurableDialogBox, PluginSettings
import threading
from .recogspeech import SpeechRecogniser
from .saveasdialog import FileSaver
from .setlog import logger
from .statesmod import states

gedit_plugin_path = '.local/share/gedit/plugins'


class BackgroundThread(threading.Thread):
    def __init__(self, instance):
        threading.Thread.__init__(self)
        # getting the plugin instance so we can call its functions
        self.plugin_instance = instance
        logger.debug("BG INIT")

    def run(self):
        # call the bgcallhandler in this thread
        # logger.debug(self.name + " run thread")
        self.plugin_instance.bgcallhandler()

    def stop(self):
        del self.plugin_instance
        # logger.debug(self.name + " stop thread")

    def __del__(self):
        logger.debug("BG DEL")


class DictonatorPluginActions:
    def __init__(self, f_bottom_bar_changer):
        # Constructor
        # Will update window from UIClass
        self.window = None
        # A manager to handle settings
        self.setting_manager = PluginSettings()
        # Using like a global function
        self.bottom_bar_text_set = f_bottom_bar_changer
        # each class has its own recogniser thread
        self.thread = BackgroundThread(self)
        self._thread_is_running = False
        self.demand_fix_ambient_noise = True
        self.s_recogniser = SpeechRecogniser(f_bottom_bar_changer, self.thread_run_get)
        logger.debug("Actions INIT")

    def thread_run_get(self):
        return self._thread_is_running

    def thread_run_set(self, bool_state):
        self._thread_is_running = bool_state

    def on_setup_activate(self, action):
        # Demanding noise fix
        # logger.debug("Demand noise variable set to True")
        self.on_stop_activate(action)
        self.demand_fix_ambient_noise = True

    def on_listen_activate(self, action):
        # Start recogniser thread
        if self.thread_run_get():
            self.on_stop_activate(action)
        # logger.debug('Thread Started')
        self.thread_run_set(True)
        self.thread.start()

    def on_stop_activate(self, action):
        # Stop recogniser thread
        if self.thread_run_get():
            # logger.debug('Thread Stopping')
            self.thread_run_set(False)
            self.thread.stop()
            self.thread.join()
            self.bottom_bar_text_set("Turned OFF")
            self.thread = BackgroundThread(self)
            # logger.debug('Stopped')

    def _callrecog(self):
        # Calls recognizer and gets the text output
        _textout = self.s_recogniser.recog(PluginSettings.settings)
        logger.debug("Getting States")
        _state = states.decide_state(_textout)
        return _textout, _state

    def inserttext(self, text):
        # Inserts the text in the document
        doc = self.window.get_active_document()
        doc.begin_user_action()
        doc.insert_at_cursor(text)
        doc.end_user_action()
        # logger.debug("Inserted Text")

    @staticmethod
    def _get_cursor_position(doc):
        # gets the current cursor position, Gtk+ 2.1 has this inbuilt as property
        c_mark = doc.get_insert()
        i = doc.get_iter_at_mark(c_mark)
        return i

    def on_logit_activate(self, action):
        # a fuction to test other functions
        pass

    def bgcallhandler(self):
        # Based on output by the callRecog we proceed further
        # logger.debug("Inside bgcallhandler")

        # Check if ambient noise fix was called for
        if self.demand_fix_ambient_noise:
            # logger.debug("Demanding noise fix")
            self.bottom_bar_text_set("Setting up Dictator, Please wait for a few seconds")
            self.s_recogniser.fix_ambient_noise()
            self.bottom_bar_text_set("Dict'O'nator has been setup")
            self.demand_fix_ambient_noise = False
            # logger.debug("Noise Fix Done")

        self.bottom_bar_text_set("Speak Now!")
        (text, currstate) = self._callrecog()
        # logger.debug("received text is " + text)

        if not self.thread_run_get():
            # logger.debug("Thread not running")
            self.thread.join()
            self.bottom_bar_text_set("Turned OFF")
            return

        if currstate == "start_dictation":
            self.inserttext(text)
            self.bgcallhandler()
        elif currstate == "stop_dictation":
            # logger.debug("End Background Call Handler")
            self.bottom_bar_text_set("Turned OFF")
            return
        elif currstate == "hold_dictation":
            pass
        elif currstate == "scroll_to_cursor":
            vi = self.window.get_active_view()
            vi.scroll_to_cursor()
        elif currstate == "goto_line":
            pass
        elif currstate == "undo":
            doc = self.window.get_active_document()
            if doc.can_undo():
                doc.begin_user_action()
                doc.undo()
                doc.end_user_action()
        elif currstate == "redo":
            doc = self.window.get_active_document()
            if doc.can_redo():
                doc.begin_user_action()
                doc.redo()
                doc.end_user_action()
        elif currstate == "cut_clipboard":
            vi = self.window.get_active_view()
            vi.cut_clipboard()
        elif currstate == "copy_clipboard":
            vi = self.window.get_active_view()
            vi.copy_clipboard()
        elif currstate == "paste_clipboard":
            vi = self.window.get_active_view()
            vi.paste_clipboard()
        elif currstate == "delete_selection":
            vi = self.window.get_active_view()
            vi.delete_selection()
        elif currstate == "select_all":
            vi = self.window.get_active_view()
            vi.select_all()
        elif currstate == "spacebar_input":
            self.inserttext(' ')
            self.bgcallhandler()
        elif currstate == "sentence_end":
            self.inserttext('.')
            self.bgcallhandler()
        elif currstate == "delete_line":
            doc = self.window.get_active_document()
            doc.begin_user_action()
            ei = self._get_cursor_position(doc)
            si = self._get_cursor_position(doc)
            si.set_line(ei.get_line())
            ei.forward_to_line_end()
            doc.delete(si, ei)
            doc.end_user_action()
        elif currstate == "delete_sentence":
            doc = self.window.get_active_document()
            doc.begin_user_action()
            ei = self._get_cursor_position(doc)
            si = self._get_cursor_position(doc)
            if not si.starts_sentence():
                si.backward_sentence_start()
            si.backward_char()
            ei.forward_sentence_end()
            doc.delete(si, ei)
            doc.end_user_action()
        elif currstate == "delete_word":
            doc = self.window.get_active_document()
            doc.begin_user_action()
            ei = self._get_cursor_position(doc)
            si = self._get_cursor_position(doc)
            si.backward_word_start()
            si.backward_char()
            ei.forward_word_end()
            doc.delete(si, ei)
            doc.end_user_action()
        elif currstate == "clear_document":
            doc = self.window.get_active_document()
            if not doc:
                return
            doc.begin_user_action()
            doc.set_text('')
            doc.end_user_action()
        elif currstate == "new_document":
            self.window.create_tab(True)
        elif currstate == "save_document":
            doc = self.window.get_active_document()
            # checking if the document is a new document
            if doc.is_untitled():
                self.bottom_bar_text_set("First save should be Save As...")
                FileSaver(self.window)
            else:
                doc.save(Gedit.DocumentSaveFlags(15))
        elif currstate == "save_as_document":
            FileSaver(self.window)
        elif currstate == "close_document":
            if self.window.get_active_document.is_untouched():
                self.window.close_tab(self.window.get_active_tab())
            else:
                # to prevent data loss
                self.bottom_bar_text_set("You might wanna save the document before quitting.")
        elif currstate == "force_close_document":
            self.window.close_tab(self.window.get_active_tab())
        elif currstate == "error_state":
            logger.debug("Some Error ######")
        else:
            # logger.debug("End Background Call Handler")
            self.bottom_bar_text_set("Turned OFF")
            return

    def stop(self):
        del self.window
        del self.setting_manager
        del self.bottom_bar_text_set
        del self.thread
        del self._thread_is_running
        del self.demand_fix_ambient_noise
        del self.s_recogniser

    def __del__(self):
        logger.debug("Actions DEL")


class DictonatorUI(GObject.Object, Gedit.WindowActivatable, PeasGtk.Configurable):
    __gtype_name__ = "Dictonator"
    window = GObject.property(type=Gedit.Window)

    # Defining the UI string that is to be added
    ui_str = """
                <ui>
                  <menubar name="MenuBar">
                    <menu name="ToolsMenu" action="Tools">
                      <placeholder name="ToolsOps_2">
                        <menu name="Dictonator" action="Dictonator">
                          <menuitem name="Listen" action="Listen"/>
                          <menuitem name="Stop" action="Stop"/>
                          <menuitem name="Setup Dictator" action="Setup Dictator"/>
                          <menuitem name="Logit" action="Logit"/>
                        </menu>
                      </placeholder>
                    </menu>
                  </menubar>
                </ui>
            """

    def __init__(self):
        # Main plugin Constructor
        GObject.Object.__init__(self)
        self._action_group = Gtk.ActionGroup("DictonatorPluginActions")
        self._bottom_widget = None
        # Get the plugin manager
        self.plugin_manager = DictonatorPluginActions(self.bottom_bar_text_changer)
        logger.debug('UI INIT')

    def do_update_state(self):
        self.plugin_manager.window = self.window
        self._action_group.set_sensitive(self.window.get_active_document() is not None)

    def do_activate(self):
        # Insert menu and bottom panel into gui
        self._insert_menu()
        self._insert_bottom_panel()
        # Very important window updated for manager class
        self.plugin_manager.window = self.window

    def _insert_menu(self):
        # Define actions and merge into UImanager
        actions = [
            ('Dictonator', None, 'Dictonator'),
            ("Listen", None, "Start Listening", '<Control><Alt>2', "Start Listening",
             self.plugin_manager.on_listen_activate),
            ("Stop", None, "Stop Listening", '<Control><Alt>3', "Stop Listening",
             self.plugin_manager.on_stop_activate),
            ("Setup Dictator", None, "Setup Dictator", '<Control><Alt>4', "Setup Dicatator",
             self.plugin_manager.on_setup_activate),
            ("Logit", None, "Logit", '<Control><Alt>5', "Logit",
             self.plugin_manager.on_logit_activate),
        ]

        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()
        self._action_group.add_actions(actions)
        manager.insert_action_group(self._action_group)
        # Merge the UI
        self._ui_id = manager.add_ui_from_string(self.ui_str)

    @staticmethod
    def get_icon(gtk_icon_size):
        # Get icon from disk and scale it
        icon = Gtk.Image.new_from_icon_name("dictonator", gtk_icon_size)
        return icon

    def _insert_bottom_panel(self):
        # Implement the Plugin into bottom bar
        icon = self.get_icon(Gtk.IconSize.SMALL_TOOLBAR)
        self._bottom_widget = Gtk.Label("Welcome to Dict'O'nator!  Start by speaking \"Start Dictation\"")
        panel = self.window.get_bottom_panel()
        panel.add_item(self._bottom_widget, "Dictonator", "Dict'O'nator", icon)
        panel.activate_item(self._bottom_widget)
        # Make sure that the bottom bar shows up
        panel.show()

    def do_deactivate(self):
        # Remove menu items and bottom bar
        logger.debug("DEACTIVATING")
        self._remove_menu()
        self._remove_bottom_panel()
        self._action_group = None
        self.stop()

    def _remove_menu(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_id)
        manager.remove_action_group(self._action_group)
        # Make sure the manager updates
        manager.ensure_update()

    def _remove_bottom_panel(self):
        panel = self.window.get_bottom_panel()
        panel.remove_item(self._bottom_widget)
        # logger.debug("Removed bottom bar")

    def do_create_configure_widget(self):
        # Implement the configuration box in plugin preferences
        return ConfigurableDialogBox().get_configure_box()

    def bottom_bar_text_changer(self, txt):
        # A text updater for bottom bar. Kind of a global function
        if self._bottom_widget is not None:
            self._bottom_widget.set_text(txt)
        else:
            # logger.debug("Tried to set bottom text after disabling plugin")
            pass

    def stop(self):
        self.plugin_manager.setting_manager.stop()
        self.plugin_manager.stop()
        del self.plugin_manager

    def __del__(self):
        logger.debug("UI DEL")
