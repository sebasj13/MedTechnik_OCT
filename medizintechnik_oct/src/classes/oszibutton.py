import os
import tkinter as tk
import tkinter.ttk as ttk

import usb
from PIL import Image, ImageTk


class OsziConnect(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.statusbar = self.parent.parent.statusbar

        path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "..", "images", "osc.jpg",
        )
        buttonImage = Image.open(path)
        self.photo = ImageTk.PhotoImage(buttonImage)
        self.button = ttk.Button(
            self,
            text="Oszilloskop koppeln",
            image=self.photo,
            compound=tk.TOP,
            command=self.connect,
        )
        self.button.pack(padx=120, pady=40)
        self.button.configure(state=tk.DISABLED)

    def connect(self):

        try:

            def three():
                self.statusbar.pb.stop()
                self.statusbar.pb.grid_forget()
                self.statusbar.log.grid(row=0, column=6, sticky=tk.W)
                self.statusbar.log.configure(
                    text="Oszilloskop erfolgreich gekoppelt!", fg="green"
                )
                self.parent.parent.oszi_connected.set(2)
                self.statusbar.set_status("oszi", 2)

            def two():
                self.statusbar.log.grid_forget()
                self.statusbar.pb.grid(row=0, column=6, sticky=tk.W)
                self.statusbar.pb.start(2)
                try:
                    try:
                        self.parent.parent.osc = usb.core.find(
                            idVendor=1183, idProduct=20570
                        )
                        self.parent.parent.osc.set_configuration()
                        usb.util.claim_interface(self.parent.parent.osc, 0)
                    except usb.core.USBError(
                        "libusb0-dll:err [claim_interface] could not claim interface 0, win error: Die angeforderte Ressource wird bereits verwendet.\r\n"
                    ):
                        pass
                except TypeError:
                    self.statusbar.pb.stop()
                    self.statusbar.pb.grid_forget()
                    self.statusbar.log.grid(row=0, column=6, sticky=tk.W)
                    self.statusbar.log.configure(
                        text="Verbindung belegt. Oszilloskop neu anschließen!", fg="red"
                    )
                    self.parent.parent.oszi_connected.set(1)
                    self.statusbar.set_status("oszi", 1)
                    return
                self.after(2500, lambda: three())

            self.button.configure(state=tk.DISABLED)
            self.statusbar.log.configure(fg="black")
            self.statusbar.log.configure(text="Koppeln an Oszilloskop...")
            self.after(1000, lambda: two())

        except self.parent.parent.osc == None:
            self.statusbar.log.configure(
                text="Fehler beim koppeln des Oszilloskops!", fg="red"
            )
            return
        except Exception:
            self.statusbar.log.configure(
                text="Fehler beim koppeln des Oszilloskops!", fg="red"
            )
            return
