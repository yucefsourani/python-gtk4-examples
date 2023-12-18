# Gtk.Label

```python
import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk,Gio,Pango

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.set_default_size(100,100)
        self.app_ = self.get_application()
        
        self.main_vertical_box = Gtk.Box.new( Gtk.Orientation.VERTICAL,5)
        self.set_child(self.main_vertical_box)
        
        self.text_label1 = Gtk.Label.new("Gtk.Label Example 111 111 111 1111 111 111 111 111 111 111 111 11")
        self.text_label1.props.wrap = True
        self.text_label1.set_wrap_mode(Pango.WrapMode.WORD)
        # https://lazka.github.io/pgi-docs/Pango-1.0/enums.html#Pango.WrapMode
        self.main_vertical_box.append(self.text_label1)
    
        
        self.wrap_or_ellipsize_button = Gtk.Button.new()
        self.wrap_or_ellipsize_button.set_label("Ellipsize Text") 
        self.wrap_or_ellipsize_button.connect("clicked",self.on_wrap_or_ellipsize_button_clicked)
        self.main_vertical_box.append(self.wrap_or_ellipsize_button)

    def on_wrap_or_ellipsize_button_clicked(self,wrap_or_ellipsize_clicked_button):
        if self.text_label1.props.wrap: # if True
            self.text_label1.props.wrap = False
            self.text_label1.set_ellipsize( Pango.EllipsizeMode.END)
            # https://lazka.github.io/pgi-docs/Pango-1.0/enums.html#Pango.EllipsizeMode
            wrap_or_ellipsize_clicked_button.set_label("Wrap Text") 
        else:
            self.text_label1.set_ellipsize( Pango.EllipsizeMode.NONE)
            self.text_label1.props.wrap = True
            wrap_or_ellipsize_clicked_button.set_label("Ellipsize Text")
    
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

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/label/Screenshot.png "Screenshot")

[Gtk.label](https://lazka.github.io/pgi-docs/index.html#Gtk-4.0/classes/Label.html)
