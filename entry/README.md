# Gtk.Entry

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
        
        model = Gtk.ListStore.new([str])
        for i in ("Admin","admin","Administrator","administrator"):
            model.append([i])
        completion = Gtk.EntryCompletion.new()
        completion.set_minimum_key_length(1) # the minimum length of the key in order to start completing
        completion.set_model(model)
        completion.set_text_column(0) # first item in [str] to show
        
        self.entry  =  Gtk.Entry.new()
        self.main_vertical_box.append(self.entry)
        self.entry.set_completion(completion)
        self.entry.set_has_frame(True) # True is default
        self.entry.props.margin_start  = 20
        self.entry.props.margin_end    = 20
        self.entry.props.margin_top    = 20
        self.entry.props.margin_bottom = 20
        self.entry.set_placeholder_text("Enter Username...")
        self.entry.set_alignment(0) #start center end from 0 to 1 example : 0.1 0.2 0.3 ...
        self.entry.set_icon_from_icon_name( Gtk.EntryIconPosition.SECONDARY ,"edit-clear") 
        self.entry.set_icon_tooltip_markup( Gtk.EntryIconPosition.SECONDARY ,"<b>Clear Text</b>") # markup bold
        self.entry.set_input_purpose( Gtk.InputPurpose.FREE_FORM  )  # This information is useful for on-screen keyboards and similar input methods to decide which keys should be presented to the user.
        self.entry.set_max_length( 20  )  # max char 20
        self.entry.connect("icon_press",self.on_icon_pressed)
        
        self.entry_buffer = self.entry.get_buffer()
        self.entry_buffer.connect("notify::text",self.on_text_changed)
        
    def on_icon_pressed(self,entry,icon_pos):
        if icon_pos == Gtk.EntryIconPosition.SECONDARY:
            self.entry_buffer.set_text("",0) # clear
            
    def on_text_changed(self,buffer_,prop):
        print(buffer_.props.text)
        text_length = len(buffer_.props.text)
        self.entry.set_progress_fraction(text_length*0.05) # optional#  max text length 20 look at line 36 - fraction from 0 to 1 
        
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

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/entry/Screenshot.png "Screenshot")

[Gtk.Entry](https://amolenaar.github.io/pgi-docgen/index.html#Gtk-4.0/classes/Entry.html)
