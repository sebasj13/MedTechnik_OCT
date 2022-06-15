import os
import threading
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

import numpy as np

from ..KDC101.rasterscan import ramp_arrays


class MotorControl(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent.parent
        self.statusbar = self.parent.statusbar

        self.motor1label = ttk.Label(self, text="Axialer Motor")
        self.motor2label = ttk.Label(self, text="Transversaler Motor")

        self.position1label = ttk.Label(self, text="Position:")
        self.position2label = ttk.Label(self, text="Position:")

        self.motor1label.grid(pady=2, row=0, column=0, columnspan=2, sticky=tk.N)
        self.motor2label.grid(pady=2, row=0, column=2, columnspan=2, sticky=tk.N)

        self.position1label.grid(pady=2, row=1, column=0, columnspan=2, sticky=tk.W)
        self.position2label.grid(pady=2, row=1, column=2, columnspan=2, sticky=tk.W)

        self.home1 = ttk.Button(self, text="Home", command=lambda: self.home(1))
        self.jog1 = ttk.Button(self, text="Ausfahren", command=lambda: self.jog(1, 1))
        self.jogback1 = ttk.Button(
            self, text="Einfahren", command=lambda: self.jog(1, 0)
        )
        self.stop1 = ttk.Button(self, text="Stop", command=lambda: self.stop(1))
        self.motor1entry = ttk.Entry(self, width=10)
        self.motor1move = ttk.Button(
            self, text="Anfahren  [mm]:", command=lambda: self.move_to(1)
        )

        self.home1.grid(pady=2, row=2, column=0, columnspan=2, sticky=tk.N)
        self.jog1.grid(pady=2, row=3, column=0, columnspan=2, sticky=tk.N)
        self.jogback1.grid(pady=2, row=4, column=0, columnspan=2, sticky=tk.N)
        self.stop1.grid(pady=2, row=5, column=0, columnspan=2, sticky=tk.N)
        self.motor1entry.grid(pady=2, row=6, column=1, sticky=tk.W)
        self.motor1move.grid(pady=2, row=6, column=0, sticky=tk.E)

        self.home2 = ttk.Button(self, text="Home", command=lambda: self.home(2))
        self.jog2 = ttk.Button(self, text="Ausfahren", command=lambda: self.jog(2, 1))
        self.jogback2 = ttk.Button(
            self, text="Einfahren", command=lambda: self.jog(2, 0)
        )
        self.stop2 = ttk.Button(self, text="Stop", command=lambda: self.stop(2))
        self.motor2entry = ttk.Entry(self, width=10)
        self.motor2move = ttk.Button(
            self, text="Anfahren [mm]:", command=lambda: self.move_to(2)
        )

        self.home2.grid(pady=2, row=2, column=2, columnspan=2, sticky=tk.N)
        self.jog2.grid(pady=2, row=3, column=2, columnspan=2, sticky=tk.N)
        self.jogback2.grid(pady=2, row=4, column=2, columnspan=2, sticky=tk.N)
        self.stop2.grid(pady=2, row=5, column=2, columnspan=2, sticky=tk.N)
        self.motor2entry.grid(pady=2, row=6, column=3, sticky=tk.W)
        self.motor2move.grid(pady=2, row=6, column=2, sticky=tk.E)

        self.seperator = tk.Canvas(self, bg="black", height=2, width=390)
        self.seperator.grid(row=7, column=0, columnspan=4)

        self.rowlabel = ttk.Label(self, text="Zeilen:")
        self.rowsteplabel = ttk.Label(self, text="Schrittweite [mm]:")
        self.collabel = ttk.Label(self, text="Spalten:")
        self.colsteplabel = ttk.Label(self, text="Schrittweite [mm]:")

        self.rowlabel.grid(sticky=tk.N, row=8, column=0)
        self.rowsteplabel.grid(sticky=tk.N, row=8, column=1)
        self.collabel.grid(sticky=tk.N, row=8, column=2)
        self.colsteplabel.grid(sticky=tk.N, row=8, column=3)

        self.rowentry = ttk.Entry(self, width=9)
        self.rowstepentry = ttk.Entry(self, width=9)
        self.colentry = ttk.Entry(self, width=9)
        self.colstepentry = ttk.Entry(self, width=9)

        self.rowentry.grid(sticky=tk.N, row=9, column=0)
        self.rowstepentry.grid(sticky=tk.N, row=9, column=1)
        self.colentry.grid(sticky=tk.N, row=9, column=2)
        self.colstepentry.grid(sticky=tk.N, row=9, column=3)

        self.savevar = tk.BooleanVar(self)
        self.savevar.set(False)
        self.savebutton = ttk.Checkbutton(
            self, variable=self.savevar, text="Speichern?", command=self.save
        )
        self.savebutton.grid(row=10, column=2)
        self.rampbutton = ttk.Button(
            self,
            text="Raster",
            command=lambda: threading.Thread(target=lambda: self.ramp).start(),
        )
        self.rampbutton.grid(sticky=tk.N, row=10, columnspan=2, column=0, pady=10)
        self.channelvar = tk.BooleanVar(self)
        self.channelvar.set(False)
        self.channeldict = {False: 1, True: 2}
        self.channeltext = tk.StringVar(self)
        self.channeltext.set(f"Kanal {self.channeldict[self.channelvar.get()]}")
        self.channelbutton = ttk.Button(
            self, text=self.channeltext.get(), command=self.channel
        )
        self.channelbutton.grid(row=10, column=3)

        self.after(250, lambda: threading.Thread(target=self.position).start())

    def position(self):
        try:
            self.position1label.configure(
                text=f"Position: {float(self.parent.axial_motor.get_position())/1000:4.3f} mm"
            )
            self.position1label.configure(
                text=f"Position: {float(self.parent.transversal_motor.get_position())/1000:4.3f} mm"
            )
        except Exception:
            pass
        finally:
            self.after(250, lambda: threading.Thread(target=self.position).start())

    def save(self):
        if self.parent.osziframe.scope == None:
            self.savevar.set(False)
            self.parent.statusbar.log.configure(
                text="Osziloskop nicht angeschlossen!", fg="red"
            )

    def channel(self):
        self.channelvar.set(not self.channelvar.get())
        self.channeltext.set(f"Kanal {self.channeldict[self.channelvar.get()]}")
        self.channelbutton.configure(text=self.channeltext.get())

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
            self.parent.axial_motor.move_to(float(self.motor1entry.get()) / 1000)

        else:
            self.parent.transversal_motor.move_to(float(self.motor2entry.get()) / 1000)

    def ramp(self):

        try:
            if (
                self.parent.axial_motor == None
                and self.parent.transversal_motor == None
            ):
                return
        except Exception as e:
            print(e)
            return

        if self.savevar.get() == True:
            desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
            folder_selected = filedialog.askdirectory(initialdir=desktop)

        def three():
            try:
                self.parent.axial_motor.move_to(start[0])
                self.parent.transversal_motor.move_to(start[1])
            except Exception:
                pass
            self.parent.statusbar.pb.grid_forget()
            self.parent.statusbar.log.configure(
                text="Rasterscan abgeschlossen!", fg="green"
            )
            self.parent.statusbar.log.grid(row=0, column=6, sticky=tk.W)
            self.parent.statusbar.pb["value"] = 0
            self.parent.statusbar.pb.configure(mode="indeterminate")
            return

        def two(axial, transversal, cols, rows):

            self.parent.statusbar.log.grid_forget()
            self.parent.statusbar.pb.configure(mode="determinate")
            self.parent.statusbar.pb.grid(row=0, column=6, sticky=tk.W)
            try:
                header = f"Kanal {self.channeldict[self.channelvar.get()]}\nZeit in {self.parent.osziframe.scope.timebase_unit}\nAmplitude in {self.parent.osziframe.scope.CH1.volts_per_div_unit}"
            except Exception:
                header = ""

            for i in range(len(axial)):
                try:
                    self.parent.axial_motor.move_to(axial[i] + start[0])
                except Exception:
                    pass
                try:
                    self.parent.transversal_motor.move_to(transversal[i] + start[1])
                except Exception:
                    pass
                try:
                    self.parent.axial_motor.wait_for_stop()
                except Exception:
                    pass
                try:
                    self.parent.transversal_motor.wait_for_stop()
                except Exception:
                    pass
                try:
                    if self.savevar.get() == True:
                        data = self.parent.osziframe.scope.ReadScaledSampleData(
                            self.channeldict[self.channelvar.get()]
                        )
                        np.savetxt(
                            os.path.join(
                                folder_selected, f"{rows}x{cols}_Rasterscan_{i}.txt"
                            ),
                            np.transpose([data[0], data[1]]),
                            fmt="%10.5f",
                            header=header,
                        )
                except Exception as e:
                    pass
                self.parent.statusbar.pb["value"] += 100 / len(axial)
                self.parent.root.update_idletasks()

            self.after(1000, three)

        cols = int(self.colentry.get())
        colstep = float(self.colstepentry.get()) / 1000
        rows = int(self.rowentry.get())
        rowstep = float(self.rowstepentry.get()) / 1000
        start = [0, 0]
        try:
            start[0] = self.parent.axial_motor.get_position()
        except Exception:
            pass
        try:
            start[1] = self.parent.transversal_motor.get_position()
        except Exception:
            pass

        axial, transversal = ramp_arrays(cols, rows)
        axial, transversal = axial * rowstep, transversal * colstep

        self.parent.statusbar.log.configure(
            text=f"Fahre {cols}x{rows} Rampe ...", fg="black"
        )
        self.after(1000, lambda: two(axial, transversal, cols, rows))

