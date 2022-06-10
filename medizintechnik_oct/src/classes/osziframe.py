import threading
import tkinter as tk
import tkinter.ttk as ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class OsziControl(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent.parent
        self.statusbar = self.parent.statusbar
        self.scope = None
        self.columnconfigure(0, pad=10)
        self.startbutton = ttk.Button(self, text="Start", command=self.start)
        self.startbutton.grid(row=0, column=0, sticky=tk.W)
        self.lockbutton = ttk.Button(self, text="Sperren", command=self.lock)
        self.lockbutton.grid(row=1, column=0, sticky=tk.W)
        self.previewbutton1 = ttk.Button(
            self, text="Kanal 1", command=lambda: self.preview(1)
        )
        self.previewbutton1.grid(row=2, column=0, sticky=tk.W)
        self.previewbutton2 = ttk.Button(
            self, text="Kanal 2", command=lambda: self.preview(2)
        )
        self.previewbutton2.grid(row=3, column=0, sticky=tk.W)
        self.screenshotbutton = ttk.Button(
            self, text="Screenshot", command=self.screenshot
        )
        self.screenshotbutton.grid(row=4, column=0, sticky=tk.W)
        self.figure = plt.Figure(figsize=(3, 2), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(
            row=0, rowspan=5, column=1, pady=(10, 10), sticky=tk.NSEW,
        )
        self.toolbarFrame = tk.Frame(master=self)
        self.toolbarFrame.grid(row=5, column=0, columnspan=2, sticky=tk.W, padx=10)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        # self.ax.set_title("Vorschau")

    def start(self):

        state = self.startbutton.cget("text")

        if state == "Start":

            self.scope.StartAcquisition()
            self.startbutton.configure(text="Stop")

        else:
            self.scope.StopAcquisition()
            self.startbutton.configure(text="Start")

    def lock(self):

        state = self.lockbutton.cget("text")

        if state == "Sperren":
            self.scope.LockControlPanel()
            self.lockbutton.configure(text="Entsperren")

        else:
            self.scope.UnLockControlPanel()
            self.lockbutton.configure(text="Sperren")

    def preview(self, channel):

        self.ax.clear()
        color = {1: "yellow", 2: "blue"}
        ch_data = self.scope.ReadScaledSampleData(channel)
        unit = getattr(self.scope, f"CH{channel}").volts_per_div_unit
        self.ax.set_xlabel(f"{self.scope.timebase_unit}", x=0.9, y=-0.01)
        self.ax.set_ylabel(f"{unit}", x=-0.005, y=0.46)
        self.ax.yaxis.set_label_position("right")
        self.ax.xaxis.set_label_position("top")
        self.ax.plot(ch_data[0], ch_data[1], color=color[channel], label=f"CH{channel}")
        self.ax.grid()
        self.ax.legend()
        self.canvas.draw()
        plt.subplots_adjust(left=0.2, bottom=0.2)
        return

    def screenshot(self):

        img = self.scope.Screenshot()
        threading.Thread(target=lambda: img.show()).start()
        return
