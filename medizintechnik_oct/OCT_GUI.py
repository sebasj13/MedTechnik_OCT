# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 19:12:41 2022

@author: sebas
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 28 10:54:31 2022

@author: Sebastian Schäfer
@institution: Martin-Luther-Universität Halle-Wittenberg
@email: sebastian.schaefer@student.uni-halle.de
"""

import os
import threading
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import DISABLED, messagebox

import usb
from pylablib.devices import Thorlabs

from .src.classes.holderframe import HolderFrame
from .src.classes.motorbutton import MotorConnect
from .src.classes.motorframe import MotorControl
from .src.classes.oszibutton import OsziConnect
from .src.classes.osziframe import OsziControl
from .src.classes.statusbar import Statusbar


class OCT_GUI:
    def __init__(self):

        self.root = tk.Tk()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = 800
        height = 300
        self.root.resizable(False, False)
        x = screen_width // 2 - width // 2
        y = screen_height // 2 - height // 2
        self.root.geometry(f"{width}x{height}+{x-25}+{y}")
        self.root.state("normal")
        self.root.title("OCT Steuerung")

        ttk.Style(self.root)
        self.root.tk.call(
            "source",
            str(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "src",
                    "AzureTTK",
                    "azure.tcl",
                )
            ),
        )

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.menubar = tk.Menu(self.root, tearoff=False)

        self.connectmenu = tk.Menu(self.menubar, tearoff=False)
        self.connectmenu.add_command(
            label="Verbinden", command=lambda: print("Verbinden")
        )

        self.menubar.add_cascade(label="Verbinden", menu=self.connectmenu)
        self.menubar.add_command(label="Status", command=self.switch)

        self.root.config(menu=self.menubar)

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.statusbar = Statusbar(self)
        self.statusbar.grid(row=1, sticky=tk.NSEW)

        self.frame = HolderFrame(self)

        self.frame_left = OsziConnect(self.frame)
        self.frame_right = MotorConnect(self.frame)
        self.seperator = tk.Canvas(self.frame, bg="black", height=300, width=2)
        self.frame_left.grid(row=0, column=0, sticky=tk.NW)
        self.frame_right.grid(row=0, column=2, sticky=tk.NW)
        self.seperator.grid(row=0, column=1, sticky=tk.N)

        self.frame.grid(row=0)

        self.osziframe = OsziControl(self.frame)
        self.motorframe = MotorControl(self.frame)

        self.oszi_connected = tk.DoubleVar(value=0)
        self.axial_motor_connected = tk.DoubleVar(value=0)
        self.transversal_motor_connected = tk.DoubleVar(value=0)
        self.oszi_log = 0
        self.axial_motor_log = 0
        self.transversal_motor_log = 0
        self.osc = None
        self.axial_motor = None
        self.transversal_motor = None

        self.watchdog = threading.Thread(target=self.connection_status()).start()

    def switch(self):

        if self.statusbar.pb.winfo_ismapped():
            self.statusbar.pb.grid_forget()
            self.statusbar.log.grid(row=0, column=6, sticky=tk.W)

        else:
            self.statusbar.log.grid_forget()
            self.statusbar.pb.grid(row=0, column=6, sticky=tk.W)

    def button_state(self, column, state):

        columndict = {"axial": 0, "transversal": 2}
        statedict = {False: tk.DISABLED, True: tk.NORMAL}
        for row in [0, 1, 2, 3, 4, 5]:
            for widget in self.motorframe.grid_slaves(
                column=columndict[column], row=row
            ):
                if isinstance(widget, ttk.Button):
                    widget.configure(state=statedict[state])

        posentry = self.motorframe.grid_slaves(row=8)[0 + columndict[column]]
        stepentry = self.motorframe.grid_slaves(row=8)[1 + columndict[column]]
        if state == False:
            posentry.delete(0, tk.END)
            stepentry.delete(0, tk.END)
            posentry.insert(0, 1)
            stepentry.insert(0, 1)
            posentry.config(state=tk.DISABLED)
            stepentry.config(state=tk.DISABLED)
        else:
            posentry.config(state=tk.NORMAL)
            stepentry.config(state=tk.NORMAL)
            posentry.delete(0, tk.END)
            stepentry.delete(0, tk.END)

        return

    def connection_status(self):

        oszi = usb.core.find(idVendor=1183, idProduct=20570)

        if oszi == None:
            self.osc = None
            if self.osziframe.winfo_ismapped():
                self.osziframe.grid_forget()
                self.frame_left.grid(row=0, column=0, sticky=tk.NW)
            if self.oszi_connected.get() != 0:
                self.oszi_connected.set(0)
                if self.statusbar.log.cget("text") != "Oskilloskop getrennt!":
                    if self.oszi_log != self.oszi_connected.get():
                        self.statusbar.log.configure(
                            text="Oszilloskop getrennt!", fg="red"
                        )

            self.oszi_log = self.oszi_connected.get()
            self.statusbar.set_status("oszi", 0)
            self.frame_left.button.configure(state=tk.DISABLED)
        else:
            if self.oszi_connected.get() == 2:
                if not self.osziframe.winfo_ismapped():
                    self.frame_left.grid_forget()
                    self.osziframe.grid(row=0, column=0, sticky=tk.NW)
                self.frame_left.button.configure(state=tk.DISABLED)
            else:
                if self.osziframe.winfo_ismapped():
                    self.osziframe.grid_forget()
                    self.frame_left.grid(row=0, column=0, sticky=tk.NW)
                self.frame_left.button.configure(state=tk.DISABLED)
                self.oszi_connected.set(1)
                if self.statusbar.log.cget("text") != "Oskilloskop verbunden!":
                    if self.oszi_log != self.oszi_connected.get():
                        self.statusbar.log.configure(
                            text="Oszilloskop verbunden!", fg="orange"
                        )

                self.oszi_log = self.oszi_connected.get()
                self.statusbar.set_status("oszi", 1)
                self.frame_left.button.configure(state=tk.NORMAL)

        motors = Thorlabs.list_kinesis_devices()

        if motors == []:
            if self.motorframe.winfo_ismapped():
                self.motorframe.grid_forget()
                self.frame_right.grid(row=0, column=2, sticky=tk.NW)
            self.axial_motor = None
            self.transversal_motor = None
            self.axial_motor_connected.set(0)
            self.transversal_motor_connected.set(0)
            if self.axial_motor_connected.get() != 0:
                if self.statusbar.log.cget("text") != "Axialer Motor getrennt!":
                    if self.axial_motor_log != self.axial_motor_connected.get():
                        self.statusbar.log.configure(
                            text="Axialer Motor getrennt!", fg="red"
                        )

            if self.transversal_motor_connected.get() != 0:
                if self.statusbar.log.cget("text") != "Transversaler Motor getrennt!":
                    if (
                        self.transversal_motor_log
                        != self.transversal_motor_connected.get()
                    ):
                        self.statusbar.log.configure(
                            text="Transversaler Motor getrennt!", fg="red"
                        )

                        self.transversal_motor_log[0] = 1

            self.axial_motor_log = self.axial_motor_connected.get()
            self.statusbar.set_status("axial_motor", 0)
            self.transversal_motor_log = self.transversal_motor_connected.get()
            self.statusbar.set_status("transversal_motor", 0)
            self.root.after(1000, lambda: self.connection_status())
            self.frame_right.button.configure(state=tk.DISABLED)

            self.button_state("axial", False)
            self.button_state("transversal", False)

            return

        self.frame_right.button.configure(state=tk.NORMAL)

        if (
            len(motors) == 2
            and (
                self.axial_motor_connected.get() == 2
                and self.transversal_motor_connected.get() == 1
            )
        ) or (
            len(motors) == 2
            and (
                self.axial_motor_connected.get() == 1
                and self.transversal_motor_connected.get() == 2
            )
        ):
            if self.motorframe.winfo_ismapped():
                if self.axial_motor_connected.get() == 1:
                    try:
                        self.axial_motor = Thorlabs.KinesisMotor(
                            "27003287", scale="stage"
                        )
                        self.statusbar.log.configure(
                            text="Axialer Motor wieder gekoppelt", fg="green"
                        )
                        self.statusbar.set_status("axial_motor", 2)
                        self.axial_motor_connected.set(2)
                        self.axial_motor_log = self.axial_motor_connected.get()
                        self.button_state("axial", True)

                    except Exception:
                        self.statusbar.log.configure(
                            text="Erneutes koppeln fehlgeschlagen!", fg="red"
                        )
                elif self.transversal_motor_connected.get() == 1:
                    try:
                        self.transversal_motor = Thorlabs.KinesisMotor(
                            "27001138", scale="stage"
                        )
                        self.statusbar.log.configure(
                            text="Transversaler Motor wieder gekoppelt", fg="green"
                        )
                        self.statusbar.set_status("transversal_motor", 2)
                        self.transversal_motor_connected.set(2)
                        self.transversal_motor_log = (
                            self.transversal_motor_connected.get()
                        )
                        self.button_state("transversal", True)
                    except Exception:
                        self.statusbar.log.configure(
                            text="Erneutes koppeln fehlgeschlagen!", fg="red"
                        )
            self.root.after(1000, lambda: self.connection_status())
            return

        for motor in motors:
            if motor[0] == "27003287":
                if self.axial_motor_connected.get() == 2:
                    if not self.motorframe.winfo_ismapped():
                        self.frame_right.grid_forget()
                        self.motorframe.grid(row=0, column=2, sticky=tk.NW)
                        self.button_state("axial", True)
                else:
                    self.axial_motor_connected.set(1)
                    if self.statusbar.log.cget("text") != "Axialer Motor verbunden!":
                        if self.axial_motor_log != self.axial_motor_connected.get():
                            self.statusbar.log.configure(
                                text="Axialer Motor verbunden!", fg="orange"
                            )

                    self.axial_motor_log = self.axial_motor_connected.get()
                    self.statusbar.set_status("axial_motor", 1)
                    self.frame_right.button.configure(state=tk.NORMAL)
                    self.button_state("axial", False)

                if len(motors) == 1:
                    if self.transversal_motor_connected.get() != 0:
                        self.transversal_motor_connected.set(0)
                        if (
                            self.statusbar.log.cget("text")
                            != "Transversaler Motor getrennt!"
                        ):
                            if (
                                self.transversal_motor_log
                                != self.transversal_motor_connected.get()
                            ):
                                self.statusbar.log.configure(
                                    text="Transversaler Motor getrennt!", fg="red"
                                )

                    self.transversal_motor = None
                    self.transversal_motor_log = self.transversal_motor_connected.get()
                    self.statusbar.set_status("transversal_motor", 0)
                    self.button_state("transversal", False)
            elif motor[0] == "27001138":
                if self.transversal_motor_connected.get() == 2:
                    if self.axial_motor_connected.get() == 2:
                        if not self.motorframe.winfo_ismapped():
                            self.frame_right.grid_forget()
                            self.motorframe.grid(row=0, column=2, sticky=tk.NW)
                            self.button_state("transversal", True)
                else:
                    self.transversal_motor_connected.set(1)
                    if (
                        self.statusbar.log.cget("text")
                        != "Transversaler Motor verbunden!"
                    ):
                        if (
                            self.transversal_motor_log
                            != self.transversal_motor_connected.get()
                        ):
                            self.statusbar.log.configure(
                                text="Transversaler Motor verbunden!", fg="orange"
                            )

                    self.transversal_motor_log = self.transversal_motor_connected.get()
                    self.statusbar.set_status("transversal_motor", 1)
                    self.frame_right.button.configure(state=tk.NORMAL)
                    self.button_state("transversal", False)
                if len(motors) == 1:
                    if self.axial_motor_connected.get() != 0:
                        self.axial_motor_connected.set(0)
                        if self.statusbar.log.cget("text") != "Axialer Motor getrennt!":
                            if self.axial_motor_log != self.axial_motor_connected.get():
                                self.statusbar.log.configure(
                                    text="Axialer Motor getrennt!", fg="red"
                                )

                    self.axial_motor == None
                    self.axial_motor_log = self.axial_motor_connected.get()
                    self.statusbar.set_status("axial_motor", 0)
                    self.button_state("axial", False)

        if (
            len(motors) == 2
            and self.axial_motor != None
            and self.transversal_motor != None
        ):
            self.frame_right.button.configure(state=tk.DISABLED)
            if not self.motorframe.winfo_ismapped():
                self.frame_right.grid_forget()
                self.motorframe.grid(row=0, column=2, sticky=tk.NW)
                self.button_state("axial", True)
                self.button_state("transversal", True)

        self.root.after(1000, lambda: self.connection_status())
        return

    def on_closing(self):
        if messagebox.askokcancel("Schließen", "Fenster schließen?"):
            try:
                self.axial_motor.close()
                self.transversal_motor.close()
            except Exception:
                pass
            self.root.destroy()

    def mainloop(self):
        self.root.mainloop()


def run():
    OCT = OCT_GUI()
    OCT.mainloop()


if __name__ == "__main__":
    run()
