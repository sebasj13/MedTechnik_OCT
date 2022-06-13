import tkinter as tk
import tkinter.ttk as ttk
from re import A
from xml.dom.minidom import Attr

import numpy as np

from ..KDC101.rasterscan import ramp_arrays


class MotorControl(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent.parent
        self.statusbar = self.parent.statusbar

        self.motor1label = ttk.Label(self, text="Axialer Motor")
        self.motor2label = ttk.Label(self, text="Transversaler Motor")

        self.motor1label.grid(pady=2, row=0, column=0, columnspan=2, sticky=tk.N)
        self.motor2label.grid(pady=2, row=0, column=2, columnspan=2, sticky=tk.N)

        self.home1 = ttk.Button(self, text="Home", command=lambda: self.home(1))
        self.jog1 = ttk.Button(self, text="Ausfahren", command=lambda: self.jog(1, 1))
        self.jogback1 = ttk.Button(
            self, text="Einfahren", command=lambda: self.jog(1, 0)
        )
        self.stop1 = ttk.Button(self, text="Stop", command=lambda: self.stop(1))
        self.motor1entry = ttk.Entry(self, width=9)
        self.motor1move = ttk.Button(
            self, text="Anfahren", command=lambda: self.move_to(1)
        )

        self.home1.grid(pady=2, row=1, column=0, columnspan=2, sticky=tk.N)
        self.jog1.grid(pady=2, row=2, column=0, columnspan=2, sticky=tk.N)
        self.jogback1.grid(pady=2, row=3, column=0, columnspan=2, sticky=tk.N)
        self.stop1.grid(pady=2, row=4, column=0, columnspan=2, sticky=tk.N)
        self.motor1entry.grid(pady=2, row=5, column=1, sticky=tk.W)
        self.motor1move.grid(pady=2, row=5, column=0, sticky=tk.E)

        self.home2 = ttk.Button(self, text="Home", command=lambda: self.home(2))
        self.jog2 = ttk.Button(self, text="Ausfahren", command=lambda: self.jog(2, 1))
        self.jogback2 = ttk.Button(
            self, text="Einfahren", command=lambda: self.jog(2, 0)
        )
        self.stop2 = ttk.Button(self, text="Stop", command=lambda: self.stop(2))
        self.motor2entry = ttk.Entry(self, width=9)
        self.motor2move = ttk.Button(
            self, text="Anfahren", command=lambda: self.move_to(2)
        )

        self.home2.grid(pady=2, row=1, column=2, columnspan=2, sticky=tk.N)
        self.jog2.grid(pady=2, row=2, column=2, columnspan=2, sticky=tk.N)
        self.jogback2.grid(pady=2, row=3, column=2, columnspan=2, sticky=tk.N)
        self.stop2.grid(pady=2, row=4, column=2, columnspan=2, sticky=tk.N)
        self.motor2entry.grid(pady=2, row=5, column=3, sticky=tk.W)
        self.motor2move.grid(pady=2, row=5, column=2, sticky=tk.E)

        self.seperator = tk.Canvas(self, bg="black", height=2, width=390)
        self.seperator.grid(row=6, column=0, columnspan=4, pady=(20, 0))

        self.collabel = ttk.Label(self, text="Spalten:")
        self.colsteplabel = ttk.Label(self, text="Schrittweilte (S):")
        self.rowlabel = ttk.Label(self, text="Zeilen:")
        self.rowsteplabel = ttk.Label(self, text="Schrittweilte (Z):")

        self.rowlabel.grid(sticky=tk.N, row=7, column=2)
        self.rowsteplabel.grid(sticky=tk.N, row=7, column=3)
        self.collabel.grid(sticky=tk.N, row=7, column=0)
        self.colsteplabel.grid(sticky=tk.N, row=7, column=1)

        self.rowentry = ttk.Entry(self, width=9)
        self.rowstepentry = ttk.Entry(self, width=9)
        self.colentry = ttk.Entry(self, width=9)
        self.colstepentry = ttk.Entry(self, width=9)

        self.colentry.grid(sticky=tk.N, row=8, column=2)
        self.rowstepentry.grid(sticky=tk.N, row=8, column=3)
        self.rowentry.grid(sticky=tk.N, row=8, column=0)
        self.colstepentry.grid(sticky=tk.N, row=8, column=1)

        self.rampbutton = ttk.Button(self, text="Raster", command=self.ramp)
        self.rampbutton.grid(sticky=tk.N, row=9, columnspan=2, column=1, pady=10)

    def home(self, motor):
        if motor == 1:
            self.parent.axial_motor.move_to(0)
        else:
            self.parent.transversal_motor.move_to(0)

    def jog(self, motor, direction):
        if motor == 1:
            self.parent.axial_motor.jog(direction)
        else:
            self.parent.transversal_motor.jog(direction)

    def stop(self, motor):
        if motor == 1:
            self.parent.axial_motor.stop()
        else:
            self.parent.transversal_motor.stop()

    def move_to(self, motor):

        if motor == 1:
            self.parent.axial_motor.move_to(float(self.motor1entry.get()))

        else:
            self.parent.transversal_motor.move_to(float(self.motor2entry.get()))

    def ramp(self):
        def three():
            self.parent.statusbar.pb.grid_forget()
            self.parent.statusbar.log.configure(
                text="Rasterscan abgeschlossen!", fg="green"
            )
            self.parent.statusbar.log.grid(row=0, column=6, sticky=tk.W)
            self.parent.statusbar.pb["value"] = 0
            self.parent.statusbar.pb.configure(mode="indeterminate")
            return

        def two(axial, transversal):

            self.parent.statusbar.log.grid_forget()
            self.parent.statusbar.pb.configure(mode="determinate")
            self.parent.statusbar.pb.grid(row=0, column=6, sticky=tk.W)

            for i in range(len(axial)):
                try:
                    self.parent.axial_motor.move_to(axial[i] + start[0])
                except AttributeError:
                    pass
                try:
                    self.parent.transversal_motor.move_to(transversal[i] + start[1])
                except AttributeError:
                    pass
                try:
                    self.parent.axial_motor.wait_for_stop()
                except AttributeError:
                    pass
                try:
                    self.parent.transversal_motor.wait_for_stop()
                except AttributeError:
                    pass
                try:
                    data = self.parent.osc.ReadScaledSampleData()
                    # np.savetxt(f"{i}.txt", np.transpose([data[0], data[1]]))
                except AttributeError:
                    pass
                self.parent.statusbar.pb["value"] += 100 / len(axial)
                self.parent.root.update_idletasks()

            self.after(1000, three)

        cols = int(self.colentry.get())
        colstep = float(self.colstepentry.get())
        rows = int(self.rowentry.get())
        rowstep = float(self.rowstepentry.get())
        start = [0, 0]
        try:
            start[0] = self.parent.axial_motor.get_position()
        except AttributeError:
            pass
        try:
            start[1] = self.parent.transversal_motor.get_position()
        except AttributeError:
            pass

        axial, transversal = ramp_arrays(cols, rows)
        axial, transversal = axial * colstep, transversal * rowstep

        self.parent.statusbar.log.configure(
            text=f"Fahre {cols}x{rows} Rampe ...", fg="black"
        )
        self.after(1000, lambda: two(axial, transversal))

