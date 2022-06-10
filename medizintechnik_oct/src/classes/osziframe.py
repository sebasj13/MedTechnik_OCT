import tkinter as tk
import tkinter.ttk as ttk


class OsziControl(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent.root)
        self.parent = parent
        self.statusbar = self.parent.statusbar
