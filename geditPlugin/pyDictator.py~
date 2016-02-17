from gi.repository import GObject, Gedit
   
   class ExamplePyPlugin(GObject.Object, Gedit.WindowActivatable):
       __gtype_name__ = "ExamplePyPlugin"
   
       window = GObject.property(type=Gedit.Window)
   
       def __init__(self):
           GObject.Object.__init__(self)
   
       def do_activate(self):
           pass
   
       def do_deactivate(self):
           pass
   
       def do_update_state(self):
           pass
