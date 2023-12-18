# Gtk.ColorButton

```python
import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk,Gio, Gdk

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_ = self.get_application()

        self.main_vertical_box = Gtk.Box.new( Gtk.Orientation.VERTICAL,10) #(orientation VERTICAL|HORIZONTAL  , spacing in pixels)
        self.set_child(self.main_vertical_box)


        self.color_button1 = Gtk.ColorButton.new()
        self.color_button1.set_use_alpha(True)
        self.color_button1.connect("color-set",self.on_color_set)
        self.main_vertical_box.append(self.color_button1)
        
        self.color_button2 = Gtk.ColorButton.new()
        self.color_button2.set_use_alpha(True)
        mycolor = Gdk.RGBA()
        mycolor.parse("rgba(255,255,255,0.30)")
        #https://lazka.github.io/pgi-docs/index.html#Gdk-4.0/classes/RGBA.html#Gdk.RGBA.parse
        self.color_button2.set_rgba(mycolor)
        
        colors_list = []
        for i in range(10):
            custom_palette_color = Gdk.RGBA()
            custom_palette_color.parse("rgba({},{},{},1.0)".format(i*10,255-(i*20),300))
            colors_list.append(custom_palette_color)
        self.color_button2.add_palette(Gtk.Orientation.HORIZONTAL,5,colors_list)
        self.color_button2.connect("color-set",self.on_color_set)
        self.main_vertical_box.append(self.color_button2)


    def on_color_set(self,color_button):
        color = color_button.get_rgba() # return Gdk.RGBA
        print(color.hash())
        print(color.to_string())
        print(color.alpha) # 0.0 to 1.0
        print(color.blue)# 0.0 to 1.0
        print(color.green)# 0.0 to 1.0
        print(color.red)# 0.0 to 1.0
        
        print("====================================")
        
        print(int(color.alpha*255))
        print(int(color.blue*255))
        print(int(color.green*255))
        print(int(color.red*255))


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

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/colorbutton/Screenshot.png "Screenshot")

[Gtk.ColorButton](https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/ColorButton.html)
