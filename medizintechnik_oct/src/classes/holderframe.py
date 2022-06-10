import tkinter as tk
import tkinter.ttk as ttk


class HolderFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent.root)
        self.parent = parent
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, minsize=399)
        self.columnconfigure(1, minsize=2)
        self.columnconfigure(2, minsize=399)
