import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttks
from enum import Enum, auto
from msfs_lights import AirplaneLights, get_airplane_light_values, set_airplane_light_value, get_airplane_altitude, is_night, is_on_ground
import logging

# logging
# Configure the logger to save messages to a file
logging.basicConfig(
    level=logging.DEBUG,
    filename='mylog.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

LOGGER = logging.getLogger(__name__)
LOGGER.info("START")

# vars
script_enabled = False
checkbox_vars = []


def update_checkboxes_and_lights():
    if not script_enabled:
        return

    light_values = get_airplane_light_values()

    cabin_lights_enabled = not is_night()
    taxi_lights_enabled = is_on_ground() and is_night()

    altitude = get_airplane_altitude()
    landing_lights_enabled = altitude < 10000 and not is_night() and not is_on_ground()

    set_airplane_light_value(AirplaneLights.CABIN, cabin_lights_enabled)
    set_airplane_light_value(AirplaneLights.TAXI, taxi_lights_enabled)
    set_airplane_light_value(AirplaneLights.LANDING, landing_lights_enabled)

    for i, light in enumerate(AirplaneLights):
        checkbox_vars[i].set(light_values[light.name])

    checkbox_vars[AirplaneLights.LANDING.value].set(landing_lights_enabled)

    # Schedule the next update in 1000 ms (1 second)
    root.after(1000, update_checkboxes_and_lights)

def toggle_script():
    global script_enabled
    script_enabled = not script_enabled
    button_text = "Disable Script" if script_enabled else "Enable Script"
    toggle_button.config(text=button_text)

    if script_enabled:
        update_checkboxes_and_lights()

def create_checkbox_grid(root):
    row, column = 0, 0
    for light in AirplaneLights:
        chk_var = tk.BooleanVar()
        checkbox_vars.append(chk_var)
        chk = ttk.Checkbutton(root, text=light.name, variable=chk_var, command=lambda var=chk_var: on_checkbox_click(var))
        chk.grid(row=row, column=column, padx=5, pady=5, sticky="w")

        column += 1
        if column > 2:
            column = 0
            row += 1

    global toggle_button
    toggle_button = ttk.Button(root, text="Enable Script", command=toggle_script)
    toggle_button.grid(row=row+1, column=1, pady=10, sticky="w")

    copyright_label = ttk.Label(root, text="Copyright 2023 - Jeremy Stevens", font=("Arial", 8))
    copyright_label.grid(row=row+2, column=1, pady=(0, 5), sticky="w")

def main():
    global root
    root = tk.Tk()
    style = ttks.Style()
    root.style = style
    root.title("Airplane Lights Control")
    root.geometry("380x150")

    create_checkbox_grid(root)
    root.mainloop()

if __name__ == "__main__":
    main()