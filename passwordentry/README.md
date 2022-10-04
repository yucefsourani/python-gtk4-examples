# Gtk.PasswordEntry

```python
import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk,Gio

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_ = self.get_application()
        self.set_default_size(600, 400)
        
        self.main_vertical_box = Gtk.Box.new( Gtk.Orientation.VERTICAL,10) #(orientation VERTICAL|HORIZONTAL  , spacing in pixels)
        self.set_child(self.main_vertical_box)
        
        self.password_entry = Gtk.PasswordEntry.new()
        self.password_entry.connect("notify::text",self.on_text_changed)
        self.password_entry.set_show_peek_icon(True)
        self.password_entry.props.placeholder_text = "Enter Password"
        self.password_entry.props.margin_start  = 20
        self.password_entry.props.margin_end    = 20
        self.password_entry.props.margin_top    = 20
        self.password_entry.props.margin_bottom = 20
        self.main_vertical_box.append(self.password_entry)
            
    def on_text_changed(self,password_entry,prop):
        print(password_entry.props.text)
        # Gtk.PasswordEntry Implement Gtk.Editable
        #https://amolenaar.github.io/pgi-docgen/Gtk-4.0/classes/Editable.html#properties

        
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

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/passwordentry/Screenshot.png "Screenshot")

[Gtk.PasswordEntry](https://amolenaar.github.io/pgi-docgen/index.html#Gtk-4.0/classes/PasswordEntry.html)
