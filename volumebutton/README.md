# Gtk.VolumeButton

```python
import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk,Gio

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_ = self.get_application()
        
        self.main_vertical_box = Gtk.Box.new( Gtk.Orientation.VERTICAL,10)
        self.set_child(self.main_vertical_box)
        
        hbox = Gtk.Box.new( Gtk.Orientation.HORIZONTAL,10)
        hbox.props.margin_start  = 20
        hbox.props.margin_end    = 20
        hbox.props.margin_top    = 20
        hbox.props.margin_bottom = 20
        #https://lazka.github.io/pgi-docs/index.html#Gtk-4.0/classes/Widget.html#Gtk.Widget.props.margin_bottom
        self.main_vertical_box.append(hbox)

        volumebutton = Gtk.VolumeButton.new()
        volumebutton.connect("value-changed",self.on_volume_value_changed)
        hbox.append(volumebutton)
        
    def on_volume_value_changed(self,volumebutton,value):
        print(value)
        
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

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/volumebutton/Screenshot.png "Screenshot")

[Gtk.VolumeButton](https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/VolumeButton.html)
