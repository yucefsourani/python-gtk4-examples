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
        
        self.headerbar = Adw.HeaderBar.new() 
        self.mainvbox.append(self.headerbar) # no headerbar in Adw.ApplicationWindow 
        
        clamp = Adw.Clamp.new()
        self.mainvbox.append(clamp)
        clamp.set_maximum_size(500) # max width of clamp and her child when maximize window is 500
        
        sw = Gtk.ScrolledWindow.new() # To scroll rows in Gtk.listbox
        clamp.set_child(sw) # max width is 500
        self.listbox = Gtk.ListBox.new()
        sw.set_child(self.listbox)
        self.listbox.props.vexpand = True
        self.listbox.set_css_classes(["boxed-list"])
        
        self.create_searchbar()
        self.create_expander_row()

    def create_searchbar(self):
        search_entry = Gtk.SearchEntry.new()
        search_entry.connect("search_changed",self.on_input_text_to_search,self.listbox) # listbox to listbox.invalidate_filter() and start filter
        self.listbox.set_filter_func(self.run_filter_row,search_entry) # run_filter_row() to filder row (search_entry to get text to search)
        
        searchbar    = Gtk.SearchBar.new()
        self.mainvbox.insert_child_after(searchbar,self.headerbar) # insert searchbar after headerbar
        searchbar.connect_entry(search_entry)
        searchbar.set_child(search_entry) # add search entry to searchbar
        searchbar.set_show_close_button(True) # show close button to close searcbar and stop filter
        searchbar.set_key_capture_widget(self) # capture keyboard input on main window focus

    def on_input_text_to_search(self,search_entry,listbox):
        listbox.invalidate_filter() # call function self.run_filter_row() ++> look at self.listbox.set_filter_func(self.run_filter_row)

    def run_filter_row(self,expander_row,search_entry):
        # run_filter_row get all expander rows in listbox (row by row) 
        text_to_search = search_entry.get_text().strip().lower()
        if len(text_to_search) == 0:
            return True# if retun True show expander_row # if text length == 0 return True(show expander_row)
        if text_to_search in expander_row.get_title().lower() or text_to_search in expander_row.get_subtitle().lower():
            return True # if retun True show expander_row
        
    def create_expander_row(self):
        for info_ in (("Microphone","Audio Input"),("Audio","Audio Output")):
            title      = info_[0]
            subtitle   = info_[1]
            action_row = Adw.ExpanderRow.new()
            self.listbox.append(action_row)
            if Adw.get_major_version() == 1 and Adw.get_minor_version() >2:
                action_row.set_title_lines(1)  # number of line before wrap title text (require libAdwaita version > 1.2)
                action_row.set_subtitle_lines(4) # number of line before wrap subtitle text (require libAdwaita version > 1.2)
            
            action_row.add_prefix(Gtk.Image.new_from_icon_name("audio-input-microphone-symbolic")) # use https://flathub.org/apps/org.gnome.design.IconLibrary
            action_row.set_title(title)
            action_row.set_subtitle(subtitle)
            
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

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/libadwaita_scale_clamp_expanderrow_searchbar/Screenshot_1.png "Screenshot")



[Adw.ApplicationWindow](https://amolenaar.github.io/pgi-docgen/index.html#Adw-1/classes/ApplicationWindow.html)


[Adw.Clamp](https://lazka.github.io/pgi-docs/index.html#Adw-1/classes/Clamp.html)


[Adw.ExpanderRow](https://lazka.github.io/pgi-docs/index.html#Adw-1/classes/ExpanderRow.html)


[Gtk.Scale](https://lazka.github.io/pgi-docs/index.html#Gtk-4.0/classes/Scale.html)


[Gtk.SearchBar](https://lazka.github.io/pgi-docs/index.html#Gtk-4.0/classes/SearchBar.html)


[Gtk.SearchEntry](https://lazka.github.io/pgi-docs/index.html#Gtk-4.0/classes/SearchEntry.html)

