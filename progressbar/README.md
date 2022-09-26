# Gtk.ProgressBar

```python
import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk,Gio

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_ = self.get_application()

        self.main_vertical_box = Gtk.Box.new( Gtk.Orientation.VERTICAL,10) #(orientation VERTICAL|HORIZONTAL  , spacing in pixels)
        self.set_child(self.main_vertical_box)

        spinner1 = Gtk.Spinner.new()
        self.main_vertical_box.append(spinner1)

        self.start_stop_spinner1_button = Gtk.ToggleButton.new_with_label("Start/Stop Spinner1")
        self.start_stop_spinner1_button.connect("toggled",self.on_start_stop_spinner1_button_toggled,spinner1)
        self.main_vertical_box.append(self.start_stop_spinner1_button)


        self.main_vertical_box.append(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL))

        spinner2 = Gtk.Spinner.new()
        self.main_vertical_box.append(spinner2)

        spinner2_hbox = Gtk.Box.new( Gtk.Orientation.HORIZONTAL,1)
        self.main_vertical_box.append(spinner2_hbox)

        self.start_spinner2_button = Gtk.ToggleButton.new_with_label("Start Spinner2")
        self.start_spinner2_button.props.hexpand = True # to horizontal expand 
        self.start_spinner2_button.connect("toggled",self.on_start_spinner2_button_toggled,spinner2)
        spinner2_hbox.append(self.start_spinner2_button)

        self.stop_spinner2_button  = Gtk.ToggleButton.new_with_label("Stop Spinner2")
        self.stop_spinner2_button.connect("toggled",self.on_stop_spinner2_button_toggled,spinner2)
        spinner2_hbox.append(self.stop_spinner2_button)

        self.start_spinner2_button.set_group(self.stop_spinner2_button)


    def on_start_stop_spinner1_button_toggled(self,start_stop_spinner1_button,spinner):
        if start_stop_spinner1_button.get_active():
            spinner.start()
        else:
            spinner.stop()

    def on_start_spinner2_button_toggled(self,start_stop_spinner1_button,spinner):
        spinner.start()

    def on_stop_spinner2_button_toggled(self,start_stop_spinner1_button,spinner):
        spinner.stop()

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
