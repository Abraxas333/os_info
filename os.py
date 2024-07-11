import tkinter as tk
from tkinter import ttk, messagebox, END, filedialog
import sys
import platform
import datetime
import csv

saved_queries = './output.csv'

class OS_Info:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Info App")
        self.root.geometry("700x600") 
        self.create_gui()
        self.info = {}

    def create_gui(self):
        self.root.update_idletasks() 

        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        options = {
            "sys modules": "modules",
            "sys recursion limit": "getrecursionlimit",
            "sys defaultencoding": "getdefaultencoding",
            "sys maxsize": "maxsize",
            "sys version": "version",
            "sys path": "path",
            "platform processor": "processor",
            "platform architecture": "architecture",
            "platform machine": "machine",
            "network name": "node",
            "OS": "platform"
        }

        self.checkbuttons = {}
        self.vars = {}

        row_limit = 3
        row = 0
        column = 0
        for key, attr in options.items():
            var = tk.BooleanVar()
            checkbutton = ttk.Checkbutton(self.root, text=key, variable=var)
            checkbutton.grid(row=row, column=column, sticky=tk.W, padx=25)
            self.checkbuttons[key] = checkbutton
            self.vars[key] = var
            row += 1
            if row > row_limit:
                row = 0
                column += 1

        self.result_box = tk.Text(self.root)
        self.result_box.grid(row=8, columnspan=3, padx=25, pady=10)

        self.button_confirm = ttk.Button(self.root, text="OK", command=self.query_info)
        self.button_confirm.grid(row=7, column=0, padx=20, pady=15, sticky=tk.W)

        self.button_export = ttk.Button(self.root, text="export", command=self.export_info)
        self.button_export.grid(row=7, column=1, padx=25, pady=15, sticky=tk.W)

        self.button_import = ttk.Button(self.root, text="import", command=self.import_info)
        self.button_import.grid(row=7, column=2, padx=25, pady=15, sticky=tk.W)

    def query_info(self):
        self.info["time"] = datetime.datetime.now()
        options_sys = {
            "sys modules": "modules",
            "sys maxsize": "maxsize",
            "sys version": "version",
            "sys path": "path",
            "sys recursion limit": "getrecursionlimit",
            "sys defaultencoding": "getdefaultencoding",
        }

        options_platform = {
            "platform processor": "processor",
            "platform architecture": "architecture",
            "platform machine": "machine",
            "network name": "node",
            "OS": "platform"
        }

        for key, var in self.vars.items():
            if var.get():
                try:
                    if key in options_sys:
                        attr = options_sys[key]
                        if "get" not in attr:
                            self.info[key] = getattr(sys, attr)
                        else:
                            self.info[key] = getattr(sys, attr)()
                    elif key in options_platform:
                        attr = options_platform[key]
                        self.info[key] = getattr(platform, attr)()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed due to: {e}")

        self.display_info()

    def save_to_csv(self, filename):
        with open(filename, 'a', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(self.info.keys())
            writer.writerow(self.info.values())

    def display_info(self):
        self.result_box.delete(1.0, tk.END)
        for key, value in self.info.items():
            self.result_box.insert(tk.END, f"{key}: {value}\n")
        self.save_to_csv(saved_queries)

    def export_info(self):
        f = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[('csv files', '*.csv'), ('All files', '*.*')])
        if f:
            with open(f, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(self.info.keys())
                writer.writerow(self.info.values())
            messagebox.showinfo("Success", f"Exported Data to: {f}")

    def import_info(self):
        f = filedialog.askopenfilename(defaultextension=".csv", filetypes=[('csv files', '*.csv'), ('All files', '*.*')])
        if f:
            with open(f, "r", newline="") as file:
                reader = csv.reader(file)
                headers = next(reader)
                values = next(reader)
                self.info = dict(zip(headers, values))
                self.display_info()
            messagebox.showinfo("Success", f"Data imported from {f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OS_Info(root)
    root.mainloop()
