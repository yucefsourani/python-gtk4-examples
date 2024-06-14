# Gio.Settings Bind Gnome Shell setting To Switch row

```python

import sys
import gi
gi.require_version("Gtk","4.0")
gi.require_version("Adw","1")
from gi.repository import Gtk,Gio,Adw

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(800, 600)
        self.app_ = self.get_application()
        
        self.mainvbox = Gtk.Box.new( Gtk.Orientation.VERTICAL,5) #(orientation VERTICAL|HORIZONTAL  , spacing in pixels)
        
        self.set_content(self.mainvbox) # no set_child in Adw.ApplicationWindow
        
        headerbar = Adw.HeaderBar.new() 
        self.mainvbox.append(headerbar) # no headerbar in Adw.ApplicationWindow 
        
        clamp = Adw.Clamp.new()
        self.mainvbox.append(clamp)
        clamp.set_maximum_size(500) # max width of clamp and her child when maximize window is 500
        
        self.listbox = Gtk.ListBox.new()
        self.listbox.set_css_classes(["boxed-list"])
        clamp.set_child(self.listbox) # max width is 500
        

        action_row = Adw.SwitchRow.new()
        self.listbox.append(action_row)
        if Adw.get_major_version() == 1 and Adw.get_minor_version() >2:
            action_row.set_title_lines(1)  # number of line before wrap title text (require libAdwaita version > 1.2)
            action_row.set_subtitle_lines(4) # number of line before wrap subtitle text (require libAdwaita version > 1.2)
        
        action_row.add_prefix(Gtk.Image.new_from_icon_name("audio-volume-overamplified-symbolic")) # use https://flathub.org/apps/org.gnome.design.IconLibrary
        action_row.set_title("Gnome Volume Above")
        action_row.set_subtitle("Allow Volume Above 100 Percent")
        
        # gsettings list-recursively  org.gnome.desktop.sound
        self.settings = Gio.Settings.new("org.gnome.desktop.sound")
        self.settings.bind("allow-volume-above-100-percent",action_row,"active", Gio.SettingsBindFlags.DEFAULT)
        # https://lazka.github.io/pgi-docs/#Gio-2.0/classes/Settings.html#Gio.Settings.bind


class MyApp(Adw.Application):
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

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/gio_settings/Screenshot.png "Screenshot")

[Gtk.ListView](https://lazka.github.io/pgi-docs/#Gio-2.0/classes/Settings.html#Gio.Settings)

[Gtk.StringList](https://lazka.github.io/pgi-docs/#Adw-1/classes/SwitchRow.html#Adw.SwitchRow)
