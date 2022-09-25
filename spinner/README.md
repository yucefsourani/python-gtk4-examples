# Gtk.Spinner

```python
import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk,Gio,GLib
import threading
import time

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_ = self.get_application()
        
        self.headerbar = Gtk.HeaderBar.new()
        self.set_titlebar(self.headerbar)
        
        self.spinner = Gtk.Spinner.new()
        self.headerbar.pack_end(self.spinner)
        
        start_button = Gtk.Button.new()
        start_button.props.label = "Start Task"
        start_button.connect("clicked",self.on_start_button_clicked)
        self.set_child(start_button)
        
    def on_start_button_clicked(self,start_button):
        threading.Thread(target=self.__thread_on_start_button_clicked,args=(start_button,)).start()
        
    def __thread_on_start_button_clicked(self,start_button):
        #self.spinner.start()
        GLib.idle_add(self.spinner.start) # use GLib.idle_add to run gtk method from another thread
        
        GLib.idle_add(start_button.set_sensitive,False) # Disable Start Task Button
        
        for i in range(5):# timeout for 5 second
            time.sleep(1)
        
        #self.spinner.stop()
        GLib.idle_add(self.spinner.stop)   # use GLib.idle_add to run gtk method from another thread
        
        GLib.idle_add(start_button.set_sensitive,True) # Enable Start Task Button
        
class MyApp(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def do_activate(self):
        active_window = self.props.active_window
        if active_window:
            active_window.present()
        else:
            self.win = MainWindow(application=self)
            self.win.present()

app = MyApp(application_id="com.github.yucefsourani.myapplicationexample",flags= Gio.ApplicationFlags.FLAGS_NONE)
app.run(sys.argv)
```

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/spinner/Screenshot.png "Screenshot")

[Gtk.Spinner](https://amolenaar.github.io/pgi-docgen/index.html#Gtk-4.0/classes/Spinner.html)
