# Gtk.Window

```python
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

QUIT = False

def quit_(window):
    global QUIT
    QUIT = True

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__()

window = MainWindow()
window.connect("close-request", quit_)
window.show()

loop = GLib.MainContext().default()
while not QUIT:
    loop.iteration(True)
```

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/window_ex/Screenshot_1.png "Screenshot")