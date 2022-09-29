# Gtk.ProgressBar

```python
import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk,Gio,GLib,Pango
import threading
import time

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_ = self.get_application()
        
        self.main_vertical_box = Gtk.Box.new( Gtk.Orientation.VERTICAL,10) #(orientation VERTICAL|HORIZONTAL  , spacing in pixels)
        self.set_child(self.main_vertical_box)
        
        
        self.progressbar1 = Gtk.ProgressBar.new()
        self.progressbar1.set_show_text(True)
        self.progressbar1.set_ellipsize(Pango.EllipsizeMode.END)
        # https://amolenaar.github.io/pgi-docgen/Pango-1.0/enums.html#Pango.EllipsizeMode
        self.main_vertical_box.append(self.progressbar1)
        
        first_progressbar_button = Gtk.Button.new()
        first_progressbar_button.props.label = "Run First ProgressBar"
        first_progressbar_button.connect("clicked",self.on_first_progressbar_button_clicked)
        self.main_vertical_box.append(first_progressbar_button)
        
        self.progressbar2 = Gtk.ProgressBar.new()
        self.progressbar2.set_pulse_step(0.5)
        self.progressbar2.set_inverted(True)
        self.main_vertical_box.append(self.progressbar2)
        
        second_progressbar_button = Gtk.Button.new()
        second_progressbar_button.props.label = "Run Second ProgressBar"
        second_progressbar_button.connect("clicked",self.on_second_progressbar_button_clicked)
        self.main_vertical_box.append(second_progressbar_button)
        
        
    def on_first_progressbar_button_clicked(self,first_progressbar_button):
        threading.Thread(target=self.__thread_first_progressbar_button_clicked,args=(first_progressbar_button,)).start()
        
    def __thread_first_progressbar_button_clicked(self,first_progressbar_button):
        # use GLib.idle_add to run gtk method from another thread
        GLib.idle_add(first_progressbar_button.set_sensitive,False) # Disable Start Task Button 
        for i in range(5):# timeout for 5 second
            fraction = self.progressbar1.get_fraction() # float between 0.0 and 1.0 (The fraction should be between 0.0 and 1.0)
            fraction += 1/5 # 1/5 = 0.2 ===> pulse 0.2 every step (0.2 0.4 0.6 0.8 1)
            GLib.idle_add(self.progressbar1.set_fraction,fraction) # The fraction should be between 0.0 and 1.0, inclusive
            GLib.idle_add(self.progressbar1.set_text,"Task Is Runnnig %{}".format(int(fraction*100)))
            time.sleep(1)
        
        GLib.idle_add(self.progressbar1.set_text,"Task Is Done %100 ...")
        GLib.idle_add(self.progressbar1.set_fraction,0.0) # reset
        GLib.idle_add(first_progressbar_button.set_sensitive,True) # Enable Start Task Button

    def on_second_progressbar_button_clicked(self,second_progressbar_button):
        threading.Thread(target=self.__thread_second_progressbar_button_clicked,args=(second_progressbar_button,)).start()
        
    def __thread_second_progressbar_button_clicked(self,second_progressbar_button):
        for i in range(20):# timeout
            GLib.idle_add(self.progressbar2.pulse)
            time.sleep(0.2)
        GLib.idle_add(self.progressbar2.set_fraction,0.0)

        
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

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/progressbar/Screenshot.png "Screenshot")

[Gtk.ProgressBar](https://amolenaar.github.io/pgi-docgen/index.html#Gtk-4.0/classes/ProgressBar.html)
