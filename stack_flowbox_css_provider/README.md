# Gtk.FlowBox

```python
import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk,Gio,Gdk

css = b"""
        .h1 {
            font-size: 24px;
        }
        .h2 {
            font-weight: 300;
            font-size: 18px;
        }
        .h3 {
            font-size: 11px;
        }
        .h4 {
            color: alpha (@text_color, 0.7);
            font-weight: bold;
            text-shadow: 0 1px @text_shadow_color;
        }
        """

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_ = self.get_application()
        self.set_default_size(600, 400)

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_display(Gdk.Display().get_default(),
                                                 style_provider, 
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.main_box = Gtk.Box.new( Gtk.Orientation.VERTICAL,0) #(orientation VERTICAL|HORIZONTAL  , spacing in pixels)
        self.set_child(self.main_box)

        self.stack = Gtk.Stack.new()
        self.stack.props.hexpand = True
        self.stack.props.vexpand = True
        data_and_categories = {
                 ("Firefox" ,"Web Browser"            ,"icons_folder/appicns_Firefox.png")    : "Internet",
                 ("Chromium","Web Browser"            ,"icons_folder/Chromium_logo.png")      : "Internet",
                 ("Brave"   ,"Web Browser"            ,"icons_folder/brave.png")              : "Internet",
                 ("Opera"   ,"Web Browser"            ,"icons_folder/Opera-logo-256x256.png") : "Internet",
                 ("Vivaldi" ,"Web Browser"            ,"icons_folder/vivaldi.png")            : "Internet",
                 ("Gimp"    ,"Image Manipulation"    ,"icons_folder/gimp.png")               : "Graphics",
                 ("Inkscape","svg Editor..."         ,"icons_folder/inkscape.png")           : "Graphics",
                 ("Krita"   ,"sketching and painting","icons_folder/krita.png")              : "Graphics",
                 ("Blender" ,"3D modeling..."        ,"icons_folder/Blender-icon.png")       : "Graphics",
                 ("Kdenlive","Video Editor..."       ,"icons_folder/kdenlive.png")           : "Graphics"
        }
        done = []
        for data,category in data_and_categories.items():
            if category not in done: # if flowbox not exist in stack
                sw  = Gtk.ScrolledWindow.new()
                flowbox = Gtk.FlowBox.new()
                sw.set_child(flowbox)
                flowbox.props.homogeneous = True
                flowbox.set_valign(Gtk.Align.START) # top to bottom
                flowbox.props.margin_start  = 20
                flowbox.props.margin_end    = 20
                flowbox.props.margin_top    = 20
                flowbox.props.margin_bottom = 20
                flowbox.props.hexpand = True
                flowbox.props.vexpand = True
                flowbox.props.max_children_per_line = 4
                flowbox.props.selection_mode = Gtk.SelectionMode.NONE
                self.stack.add_titled(sw,category,category) # Widget,name,title to show in Gtk.StackSidebar
                done.append(category)
            else: # if flowbox already exist in stack
                flowbox = self.stack.get_child_by_name(category).get_child().get_child() #Gtk.ScrolledWindow ===> get_child ====> Gtk.Viewport ===> get_child ====> Gtk.FlowBox


            icon_vbox = Gtk.Box.new( Gtk.Orientation.VERTICAL,0)

            icon      = Gtk.Image.new_from_file(data[2])#data[2] icons_folder/appicns_Firefox.png and ...
            icon.set_icon_size(Gtk.IconSize.LARGE)
            # https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/Image.html
            icon_vbox.append(icon)

            name_label = Gtk.Label.new(data[0]) #Firefox and ....
            name_label.add_css_class("h1") # look at css
            icon_vbox.append(name_label)

            summary_label = Gtk.Label.new(data[1])  #Web Browser and ....
            summary_label.add_css_class("h3") #look at css
            icon_vbox.append(summary_label)

            button = Gtk.Button.new()
            button.set_has_frame(False)
            button.set_child(icon_vbox)
            flowbox.append(button)
            button.connect("clicked",self.on_button_clicked,data[0]) 



        stack_switcher =  Gtk.StackSwitcher.new()
        stack_switcher.props.hexpand = False
        stack_switcher.props.vexpand = False
        stack_switcher.set_stack(self.stack)

        self.main_box.append(stack_switcher)
        self.main_box.append(self.stack)

    def on_button_clicked(self,button,programename):
        print(programename)

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

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/stack_flowbox_css_provider/Screenshot.png "Screenshot")

[Gtk.FlowBox](https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/FlowBox.html)

[Gtk.Stack](https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/Stack.html)

[Gtk.Image](https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/Image.html)

[Gtk.CssProvider](https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/CssProvider.html)

[Gtk.StyleContext](https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/StyleContext.html)
