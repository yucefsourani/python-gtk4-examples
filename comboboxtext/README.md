# Gtk.ComboBoxText

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
        
        data_to_show = ["Male","Female"]
        
        self.combobox_text1 = Gtk.ComboBoxText.new()
        self.main_vertical_box.append(self.combobox_text1)
        for i in data_to_show:
            self.combobox_text1.append_text(i)
        self.combobox_text1.set_active(0) # active first text in data_to_show
        
        print_button1 = Gtk.Button.new()
        print_button1.props.label = "Print actived text From ComboBoxText1 "
        print_button1.connect("clicked",self.on_print_button_clicked,self.combobox_text1)
        self.main_vertical_box.append(print_button1)

        self.combobox_text2 = Gtk.ComboBoxText.new_with_entry()
        for i in data_to_show:
            self.combobox_text2.append_text(i)
        self.combobox_text2.set_active(0)
        self.main_vertical_box.append(self.combobox_text2)
        
        print_button2 = Gtk.Button.new()
        print_button2.props.label = "Print actived text From ComboBoxText2 "
        print_button2.connect("clicked",self.on_print_button_clicked,self.combobox_text2)
        self.main_vertical_box.append(print_button2)
        
    def on_print_button_clicked(self,p_button,combobox_text):
        print(combobox_text.get_active_text())
        
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

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/comboboxtext/Screenshot.png "Screenshot")

[Gtk.ComboBoxText](https://lazka.github.io/pgi-docgen/index.html#Gtk-4.0/classes/ComboBoxText.html)
