# Gtk.Box

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

        self.about_button = Gtk.Button.new()
        self.about_button.set_label("About") # Or Change "label Propertie" self.about_button.props.label = "About"
        self.about_button.connect("clicked",self.on_about_button_clicked,"My Example App")
        self.main_vertical_box.append(self.about_button)

        self.quit_button = Gtk.Button.new_with_label("Quit")
        self.quit_button.connect("clicked",self.on_quit_button_clicked)
        self.quit_button.props.vexpand = True  # Whether to expand vertically
        # https://amolenaar.github.io/pgi-docgen/index.html#Gtk-4.0/classes/Widget.html#Gtk.Widget.props.vexpand
        self.main_vertical_box.append(self.quit_button)

    def on_about_button_clicked(self,about_clicked_button,msg):
        print(msg)

    def on_quit_button_clicked(self,quit_clicked_button):
        self.app_.quit()

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

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/Box_LAYOUT/Screenshot.png "Screenshot")

[Gtk.Box](https://amolenaar.github.io/pgi-docgen/index.html#Gtk-4.0/classes/Box.html)
