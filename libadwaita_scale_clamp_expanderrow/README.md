# Adw.ApplicationWindow

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
        
        self.create_expander_row()
        
    def create_expander_row(self):
        action_row = Adw.ExpanderRow.new()
        self.listbox.append(action_row)
        if Adw.get_major_version() == 1 and Adw.get_minor_version() >2:
            action_row.set_title_lines(1)  # number of line before wrap title text (require libAdwaita version > 1.2)
            action_row.set_subtitle_lines(4) # number of line before wrap subtitle text (require libAdwaita version > 1.2)
        
        action_row.add_prefix(Gtk.Image.new_from_icon_name("audio-input-microphone-symbolic")) # use https://flathub.org/apps/org.gnome.design.IconLibrary
        action_row.set_title("My Title")
        action_row.set_subtitle("My Subtitle")
        
        scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL,0,10,2)
        scale.set_draw_value(True)
        scale.set_value(8)
        scale.add_mark(5,Gtk.PositionType.BOTTOM,"50%")
        action_row.add_row(scale)
        
        reset_button = Gtk.Button.new_with_label("Reset")
        reset_button.connect("clicked",self.on_reset_button_clicked,scale)
        reset_button.set_css_classes(["suggested-action","pill"])
        action_row.add_action(reset_button)
    
    def on_reset_button_clicked(self,button,scale):
        scale.set_value(5)

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

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/libadwaita_scale_clamp_expanderrow/Screenshot_1.png "Screenshot")



[Adw.ApplicationWindow](https://lazka.github.io/pgi-docs/index.html#Adw-1/classes/ApplicationWindow.html)


[Adw.Clamp](https://lazka.github.io/pgi-docs/index.html#Adw-1/classes/Clamp.html)


[Adw.ExpanderRow](https://lazka.github.io/pgi-docs/index.html#Adw-1/classes/ExpanderRow.html)


[Gtk.Scale](https://lazka.github.io/pgi-docgen/index.html#Gtk-4.0/classes/Scale.html)

