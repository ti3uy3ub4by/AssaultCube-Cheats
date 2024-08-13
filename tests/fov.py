import sys
import pyMeow as pm
import tkinter as tk
from tkinter import scrolledtext

# Debug print
print("Script started")

# Initialize process and base
try:
    proc = pm.open_process("ac_client.exe")
    base = pm.get_module(proc, "ac_client.exe")["base"]
    print("Process and base initialized")
except Exception as e:
    print(f"Error initializing process and base: {e}")
    sys.exit(e)

# Define pointers and offsets
class Pointer:
    fov = 0x18A7CC

# Define cheat functions
def adjust_fov(new_fov):
    try:
        pm.w_float(proc, base + Pointer.fov, new_fov)
        print(f"FOV set to {new_fov}")
    except Exception as e:
        print(f"Error adjusting FOV: {e}")

# GUI setup
def create_gui():
    print("Creating GUI")
    root = tk.Tk()
    root.title("AssaultCube FOV Adjuster")

    # FOV Slider
    tk.Label(root, text="Adjust FOV:").grid(row=0, column=0, padx=10, pady=10)
    fov_slider = tk.Scale(root, from_=10, to=170, orient=tk.HORIZONTAL, command=lambda v: adjust_fov(float(v)))
    fov_slider.set(90)  # Default FOV value
    fov_slider.grid(row=0, column=1, padx=10, pady=10)

    # Output Window
    output_frame = tk.Frame(root)
    output_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
    output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=60, height=15)
    output_text.grid(row=0, column=0, padx=10, pady=10)

    # Redirect print to the output window
    class PrintToTkinter:
        def __init__(self, text_widget):
            self.text_widget = text_widget

        def write(self, message):
            self.text_widget.insert(tk.END, message)
            self.text_widget.see(tk.END)

        def flush(self):
            pass

    sys.stdout = PrintToTkinter(output_text)
    sys.stderr = PrintToTkinter(output_text)

    print("GUI created, starting mainloop")
    root.mainloop()

if __name__ == "__main__":
    print("Initializing GUI")
    create_gui()