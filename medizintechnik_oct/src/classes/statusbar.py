import tkinter as tk
import tkinter.ttk as ttk


class Statusbar(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent.root)
        self.parent = parent
        self.configure(borderwidth=3, relief=tk.GROOVE)
        self.columnconfigure(0, weight=18)
        self.columnconfigure(1, weight=1000)
        self.columnconfigure(2, weight=20)
        self.columnconfigure(3, weight=1000)
        self.columnconfigure(4, weight=25)
        self.columnconfigure(5, weight=1000)

        self.oszi_status_label = tk.Label(
            self,
            height=1,
            width=18,
            text="Oszilloskop: Getrennt",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
        )
        self.oszi_status_label.grid(row=0, column=0, sticky=tk.W)

        self.oszi_status_led = tk.Canvas(self, width=19, height=19, relief=tk.SUNKEN)
        self.oszi_status_LED = self.oszi_status_led.create_oval(
            4, 4, 17, 17, fill="red", outline="black"
        )
        self.oszi_status_led.grid(row=0, column=1, sticky=tk.W)

        self.axial_motor_status_label = tk.Label(
            self,
            height=1,
            width=20,
            text="Axialer Motor: Getrennt",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
        )
        self.axial_motor_status_label.grid(row=0, column=2, sticky=tk.W)

        self.axial_motor_status_led = tk.Canvas(
            self, width=19, height=19, relief=tk.SUNKEN
        )
        self.axial_motor_status_LED = self.axial_motor_status_led.create_oval(
            4, 4, 17, 17, fill="red", outline="black"
        )
        self.axial_motor_status_led.grid(row=0, column=3, sticky=tk.W)

        self.transversal_motor_status_label = tk.Label(
            self,
            height=1,
            width=25,
            text="Transversaler Motor: Getrennt",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
        )
        self.transversal_motor_status_label.grid(row=0, column=4, sticky=tk.W)

        self.transversal_motor_status_led = tk.Canvas(
            self, width=19, height=19, relief=tk.SUNKEN
        )
        self.transversal_motor_status_LED = self.transversal_motor_status_led.create_oval(
            4, 4, 17, 17, fill="red", outline="black"
        )
        self.transversal_motor_status_led.grid(row=0, column=5, sticky=tk.W)

        self.log = tk.Label(
            self,
            text="Initialisiert",
            relief="groove",
            border=2,
            anchor=tk.CENTER,
            width=37,
        )
        self.log.grid(row=0, column=6, sticky=tk.W)

        self.pb = ttk.Progressbar(
            self, orient="horizontal", mode="indeterminate", length=265
        )

    def set_status(self, label, status):

        labels = {
            "oszi": "Oszilloskop: ",
            "axial_motor": "Axialer Motor: ",
            "transversal_motor": "Transversaler Motor: ",
        }
        stati = {0: "Getrennt", 1: "Verbunden", 2: "Gekoppelt"}
        colors = {0: "red", 1: "orange", 2: "green"}

        led = getattr(self, f"{label}_status_led")
        LED = getattr(self, f"{label}_status_LED")
        indicator = getattr(self, f"{label}_status_label")
        indicator.configure(text=f"{labels[label]}" + f"{stati[status]}")
        led.itemconfig(LED, fill=f"{colors[status]}")
