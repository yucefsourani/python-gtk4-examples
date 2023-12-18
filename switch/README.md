# Gtk.Switch

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
        self.main_vertical_box.append(hbox)


        spinner = Gtk.Spinner.new()
        hbox.append(spinner)

        switch = Gtk.Switch.new()
        switch.connect("notify::active",self.on_switch_active_changed,spinner) # notify when (active propertie) changed
        hbox.append(switch)
        
    def on_switch_active_changed(self,switch,property_,spinner):
        is_active = switch.props.active # or switch.get_property(property_.name) # return True Or False
        if is_active:
            spinner.start()
        else:
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

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/switch/Screenshot.png "Screenshot")

[Gtk.Switch](https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/Switch.html)
