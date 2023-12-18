# Gtk.LinkButton

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
        
        self.linkbutton_1 = Gtk.LinkButton.new_with_label("https://arfedora.blogspot.com","MyWeb")
        self.main_vertical_box.append(self.linkbutton_1 )
        
        h_separator = Gtk.Separator.new(Gtk.Orientation.HORIZONTAL)
        self.main_vertical_box.append(h_separator )
        
        self.linkbutton_2 = Gtk.LinkButton.new("https://arfedora.blogspot.com")
        self.linkbutton_2.connect("activate-link",self.on_linkbutton_2_clicked)
        self.main_vertical_box.append(self.linkbutton_2 )
        
        self.enable_disable_linkbutton2_open_link = Gtk.ToggleButton.new_with_label("Enable/Disable Open Second Link")
        self.main_vertical_box.append(self.enable_disable_linkbutton2_open_link )
        
    def on_linkbutton_2_clicked(self,linkbutton_2 ):
        # To override the default behavior, you can connect to the ::activate-link signal and stop the propagation of the signal by returning True from your handler.
        is_active = self.enable_disable_linkbutton2_open_link.get_active()
        return is_active # if False open link if True ignore open link
        

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

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/linkbutton/Screenshot.png "Screenshot")

[Gtk.LinkButton](https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/LinkButton.html)
