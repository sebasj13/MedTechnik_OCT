import os
import tkinter as tk
import tkinter.ttk as ttk

from PIL import Image, ImageTk
from pylablib.devices import Thorlabs


class MotorConnect(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.statusbar = self.parent.parent.statusbar

        path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "..", "images", "motor.jpg",
        )
        buttonImage = Image.open(path)
        self.photo = ImageTk.PhotoImage(buttonImage)
        self.button = ttk.Button(
            self,
            text="Motoren koppeln",
            image=self.photo,
            compound=tk.TOP,
            command=self.connect,
        )
        self.button.pack(padx=120, pady=40)
        self.button.configure(state=tk.DISABLED)

    def connect(self):
        def three():
            self.statusbar.pb.stop()
            self.statusbar.pb.grid_forget()
            self.statusbar.log.grid(row=0, column=6, sticky=tk.W)
            try:
                self.parent.parent.axial_motor = Thorlabs.KinesisMotor(
                    "27003287", scale="stage"
                )
            except Exception:
                self.parent.parent.axial_motor = None
            try:
                self.parent.parent.transversal_motor = Thorlabs.KinesisMotor(
                    "27001138", scale="stage"
                )
            except Exception:
                self.parent.parent.transversal_motor = None
            if (
                self.parent.parent.axial_motor == None
                and self.parent.parent.transversal_motor == None
            ):
                self.statusbar.log.configure(
                    text="Fehler beim Koppeln der Motoren!", fg="red"
                )
            elif self.parent.parent.axial_motor == None:
                self.statusbar.log.configure(
                    text="Transversaler Motor erfolgreich gekoppelt!", fg="green"
                )
                self.after(
                    2500,
                    self.statusbar.log.configure(
                        text="Fehler beim axialen Motor!", fg="red"
                    ),
                )
                self.parent.parent.transversal_motor_connected.set(2)
                self.statusbar.set_status("transversal_motor", 2)
            elif self.parent.parent.transversal_motor == None:
                self.statusbar.log.configure(
                    text="Axialer Motor erfolgreich gekoppelt!", fg="green"
                )
                self.after(
                    2500,
                    self.statusbar.log.configure(
                        text="Fehler beim transversalen Motor!", fg="red"
                    ),
                )
                self.parent.parent.axial_motor_connected.set(2)
                self.statusbar.set_status("axial_motor", 2)
            else:
                self.statusbar.log.configure(
                    text="Motoren erfolgreich gekoppelt!", fg="green"
                )
                self.parent.parent.axial_motor_connected.set(2)
                self.statusbar.set_status("axial_motor", 2)
                self.parent.parent.transversal_motor_connected.set(2)
                self.statusbar.set_status("transversal_motor", 2)
            return

        def two():
            self.statusbar.log.grid_forget()
            self.statusbar.pb.grid(row=0, column=6, sticky=tk.W)
            self.statusbar.pb.start(2)
            self.after(2000, lambda: three())

        self.button.configure(state=tk.DISABLED)
        self.statusbar.log.configure(fg="black")
        self.statusbar.log.configure(text="Koppeln an Motoren...")
        self.after(1000, lambda: two())
