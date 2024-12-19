#!/usr/bin/env python
"""This program provides a GUI for gathering user input for enrollment.

The program uses the CustomTkinter library to display a series of pages:

1. **Acknowledgement Page**: A message asking the user to acknowledge and
   proceed with the input process.

2. **Name Input Page**: Prompts the user to enter their first and last names.

3. **Department and Building Selection Page**: Allows the user to select their
   department and building from predefined dropdown options.

4. **Save and Submit**: After gathering the necessary information, the data is
   saved into a text file.

Key notes:

* The GUI elements (labels, entry fields, dropdowns, buttons) are dynamically
  scaled based on a scaling factor for better accessibility.
* Data is currenly saved in a text file with a timestamp and the user's input.
* The program is intended for use on macOS with Python v3.9 or higher.

The program also includes helper functions for refreshing the window, clearing
widgets, and centering the window on the screen.

Dependencies:

* CustomTkinter for the GUI components.
* Pillow for image processing (background and banner images)
* Callable for typehinting
* strftime and subprocess for handling time formatting and executing system
  commands.

This project was made possible by Mehraz Ahmed with the help of Imraan Khan.
"""
import subprocess
from time import strftime
from typing import Callable

from PIL import Image
import customtkinter as ctk
from customtkinter import CTkImage

__author__ = "Mehraz Ahmed and Imraan Azad Khan"
__copyright__ = "Copyright 2024, macOS Enrollment Program"
__credits__ = ["Mehraz Ahmed", "Imraan Azad Khan"]
__license__ = "CC BY-NC-ND (https://creativecommons.org/licenses/by-nc-nd/4.0)"
__version__ = "4.0"
__maintainer__ = "Mehraz Ahmed"
__email__ = "mahmed6@ncsu.edu"
__status__ = "Development"  # "Prototype", "Development", or "Production"

ACKNOWLEDGE_MESSAGE = "College of Sciences\n\n\n"
ACKNOWLEDGE_MESSAGE += "Please answer a few quick questions to get this \
workstation properly enrolled with management."

SCALING_FACTOR = 1.5  # Scale everything by 1.5

# BACKGROUND_PATH = "./assets/4k_backgrounds/belltower-night-3840x2160.jpg"
BACKGROUND_PATH = "./assets/background.jpg"  # belltower night no writing
BANNER_PATH = "./assets/banner.png"

# Colors
REYNOLDS_RED = "#990000"

# Font
BASE_FONT = "Arial"

# Font Sizes
SMALL_FONT_SIZE = 10
SMALLER_FONT_SIZE = 11
STANDARD_FONT_SIZE = 12
LARGER_FONT_SIZE = 14

# Distances between widgets, configure from here.
DISTANCE_BETWEEN_ENTRY_X = 8
DISTANCE_BETWEEN_ENTRY_Y = 5

# Padding
STANDARD_PADY = 10
STANDARD_PADX = 20

ctk.set_appearance_mode("dark")


def scale(value):
    """
    Scales a given value by a predefined scaling factor.

    Args:
        value (float): The value to be scaled.

    Returns:
        int: The scaled value, rounded down to the nearest integer.
    """
    return int(value * SCALING_FACTOR)


def get_font(scaling: int, bold: bool = False) -> tuple[str, int, str]:
    """
    Retrieve font configuration based on scaling and style.

    Args:
        scaling (int): A scaling factor to adjust the font size.
        bold (bool, optional): Whether the font should be bold.
                               Defaults to False.

    Returns:
        tuple[str, int, str]: A tuple containing the font name,
                              the scaled size, and an optional style
                              string (e.g., "bold").
    """
    if bold:
        return (BASE_FONT, scale(scaling), "normal")

    return (BASE_FONT, scale(scaling), "bold")


def get_buildings_list(filename: str) -> list[str]:
    """Reads lines from text file and returns a list of the contents.

    Args:
        filename (str): The file name to parse

    Returns:
        list[str]: List of parsed information
    """
    info_list = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip() != "":
                info_list.append(line.strip())

    return sorted(info_list)


def load_background(tk: ctk.CTk, image_path: str):
    """
    Load and scale an image to fit the dimensions of a CTk window.

    Args:
        tk (ctk.CTk): The CTk instance whose dimensions are used
                      for scaling the image.
        image_path (str): The file path of the image to be loaded.

    Returns:
        CTkImage: A CTkImage object resized to fit the window dimensions.
    """
    img = Image.open(image_path)
    width = tk.winfo_width()
    height = tk.winfo_height()

    return CTkImage(img, size=(width, height))


def load_banner(image_path: str):
    """
    Load and resize an image to create a banner.

    Args:
        image_path (str): The file path of the image to be loaded.

    Returns:
        CTkImage: A CTkImage object resized to half of its original dimensions.
    """
    img = Image.open(image_path)
    width, height = img.size
    # resized_img = img.resize(
    #     (int(width * 0.5), int(height * 0.5)), Image.Resampling.LANCZOS)
    return CTkImage(img, size=(int(width * 0.5), int(height * 0.5)))


def refresh_window() -> None:
    """
    Refresh the program window by updating its tasks and rendering. This
    ensures that any pending updates to the UI are processed immediately.

    Returns:
        None: This function does not return a value.
    """
    root.update_idletasks()
    root.update()


def clear_root() -> None:
    """
    Clear all widgets from the root window. Removes all child widgets managed
    by the pack geometry manager and refreshes the window to reflect the
    changes.

    Returns:
        None: This function does not return a value.
    """
    for widget in root.pack_slaves():
        widget.destroy()

    refresh_window()


def get_name_label(working_frame: ctk.CTkFrame,
                   name_part: str) -> ctk.CTkLabel:
    """
    Create and returns a label widget for a name input field.

    Args:
        working_frame (ctk.CTkFrame): The frame in which the label will be
                                      placed.
        name_part (str): The part of the name (e.g., "First", "Last") to
                         display in the label.

    Returns:
        ctk.CTkLabel: The created label widget with the specified text and
                      styling.
    """
    text = f"{name_part} Name:"
    label = ctk.CTkLabel(working_frame, text=text,
                         font=get_font(STANDARD_FONT_SIZE),
                         fg_color="transparent")
    return label


def grid_position(current_widget, row: int, col: int):
    """
    Places widgets in a grid layout with scaling and padding.

    Args:
        current_widget: The widget to be placed in the grid.
        row (int): The row index in the grid layout.
        col (int): The column index in the grid layout.

    Returns:
        None: This function places the widget in the grid and does not return
              a value.
    """
    sticky = "e" if isinstance(current_widget, ctk.CTkLabel) else ""
    return current_widget.grid(row=row, column=col,
                               padx=scale(DISTANCE_BETWEEN_ENTRY_X),
                               pady=scale(DISTANCE_BETWEEN_ENTRY_Y),
                               sticky=sticky)


def get_entry_field(current_frame: ctk.CTkFrame,
                    name_part: str) -> ctk.CTkEntry:
    """
    Create and returns an entry field widget for user input.

    Args:
        current_frame (ctk.CTkFrame): The frame in which the entry field will
                                      be placed.
        name_part (str): The part of the name (e.g., "First", "Last") to be
                         used as a placeholder text.

    Returns:
        ctk.CTkEntry: The created entry field widget with the specified
                      placeholder text and styling.
    """

    return ctk.CTkEntry(current_frame, font=get_font(SMALL_FONT_SIZE),
                        fg_color="transparent",
                        placeholder_text=f"{name_part} name")


def make_button(current_frame: ctk.CTkFrame, text: str,
                command: Callable[[], None]) -> ctk.CTkButton:
    """
    Create a button widget and adds it to the specified frame.

    Args:
        current_frame (ctk.CTkFrame): The frame in which the button will be
                                      placed.
        text (str): The text to display on the button.
        command (Callable[[], None]): The function to be called when the
                                      button is clicked.

    Returns:
        ctk.CTkButton: The created button widget with the specified text,
                       command, and styling.
    """
    return ctk.CTkButton(current_frame, text=text,
                         font=get_font(SMALLER_FONT_SIZE),
                         command=command, corner_radius=16,
                         border_width=3, border_color="black",
                         border_spacing=7, anchor="center"
                         )


def name_input_page() -> None:
    """
    Display the page for entering the user's first and last name, and handles
    navigation to the next page.

    This function clears the root window, creates the necessary input fields
    for the user's first and last name, and adds a button to proceed to the
    next page after validating that both names have been entered.

    Returns:
        None: This function does not return a value.
    """
    clear_root()

    name_input_frame = ctk.CTkFrame(root)
    name_input_frame.pack(expand=True)

    # bg = load_background(root, BACKGROUND_PATH)
    # bg_label = ctk.CTkLabel(root, text="", image=bg)
    # bg_label.place(x=0, y=0)

    # banner_img = load_banner(BANNER_PATH)
    # banner_img_label = ctk.CTkLabel(root, text="", image=banner_img)
    # banner_img_label.place(x=0, y=0)

    first_name = get_name_label(name_input_frame, "First")
    grid_position(first_name, 0, 0)

    first_name_entry = get_entry_field(name_input_frame, "First")
    grid_position(first_name_entry, 0, 1)

    first_name_entry.focus()

    last_name = get_name_label(name_input_frame, "Last")
    grid_position(last_name, 1, 0)

    last_name_entry = get_entry_field(name_input_frame, "Last")
    grid_position(last_name_entry, 1, 1)

    def proceed():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        if first_name and last_name:
            building_department_input(first_name, last_name)

    name_button = make_button(name_input_frame, text="Next", command=proceed)
    name_button.grid(row=2, columnspan=2, pady=scale(STANDARD_PADY))

    root.bind("<Return>", lambda event: proceed())


def get_selection_label(current_frame: ctk.CTkFrame,
                        selection: str) -> ctk.CTkLabel:
    """
    Create and returns a label widget prompting the user to select an option.

    Args:
        current_frame (ctk.CTkFrame): The frame in which the label will be
                                      placed.
        selection (str): The option to be selected (e.g., "Department", "Role")
                         that will be displayed in the label.

    Returns:
        ctk.CTkLabel: The created label widget with the prompt text and
                      styling.
    """
    text = f"Select your {selection}:"
    label = ctk.CTkLabel(current_frame, text=text,
                         font=get_font(STANDARD_FONT_SIZE))
    label.pack(pady=scale(STANDARD_PADY), padx=scale(STANDARD_PADX))
    return label


def get_dropdown(current_frame: ctk.CTkFrame,
                 options_func: Callable[[], list[str]]
                 ) -> tuple[ctk.StringVar, ctk.CTkOptionMenu]:
    """
    Create a dropdown menu with dynamically provided options.

    Args:
        current_frame (ctk.CTkFrame): Frame for the dropdown.
        options_func (Callable[[], list[str]]): Function returning the options
                                                list.

    Returns:
        tuple[ctk.StringVar, ctk.CTkOptionMenu]: StringVar and CTkOptionMenu
                                                 instance.
    """
    dropdown_str_var = ctk.StringVar(current_frame)
    options = options_func()
    dropdown_str_var.set(options[0] if options else "")
    dropdown = ctk.CTkOptionMenu(
        current_frame, variable=dropdown_str_var, values=options)
    dropdown.pack(pady=scale(STANDARD_PADY), padx=scale(20))
    dropdown.configure(font=get_font(SMALL_FONT_SIZE))
    return dropdown_str_var, dropdown


BUILDINGS = get_buildings_list("buildings.txt")

DEPARTMENTS = {
    "Biology": "NCSU-COS-BIO",
    "Bioinformatics": "NCSU-COS-BRC",
    "Chemistry": "NCSU-COS-CHEM",
    "Mathematics": "NCSU-COS-MATH",
    "MEAS": "NCSU-COS-MEAS",
    "Physics": "NCSU-COS-PHYSICS",
    "SCO": "NCSU-COS-SCO",
    "Statistics": "NCSU-COS-STAT",
    "Other": "NCSU-COS"
}

DEPARTMENT_BUILDINGS = {
    "Biology": [],
    "Bioinformatics": [],
    "Chemistry": ["SAS Hall", "Cox Hall",
                  "Dabney Hall"],
    "Mathematics": ["SAS Hall", "Cox Hall",
                    "Dabney Hall", "Language and Computer Laboratories"],
    "MEAS": [],
    "Physics": [],
    "SCO": [],
    "Statistics": ["SAS Hall"],
    "Other": []  # All building options
}


def building_department_input(first_name: str, last_name: str) -> None:
    """Displays building and department selection, dynamically updating
    building options.

    Args:
        first_name (str): The user's first name
        last_name (str): The user's last name

    Returns:
        None: This function does not return a value.
    """
    clear_root()
    building_department_frame = ctk.CTkFrame(root)
    building_department_frame.pack(expand=True)

    get_selection_label(building_department_frame, "department")

    department_str_var = get_dropdown(
        building_department_frame, lambda: list(DEPARTMENTS.keys()))[0]

    def get_building_options():
        department = department_str_var.get()
        return DEPARTMENT_BUILDINGS.get(department, BUILDINGS)

    get_selection_label(building_department_frame, "building")

    building_str_var, building_dropdown = get_dropdown(
        building_department_frame, get_building_options)

    def update_building_dropdown(*args):  # pylint: disable=W0613
        building_dropdown.configure(values=get_building_options())
        if get_building_options():
            building_str_var.set(get_building_options()[0])

    department_str_var.trace_add("write", update_building_dropdown)

    def proceed():
        building = building_str_var.get()
        if department_str_var.get() and building:
            save_input(first_name, last_name,
                       department_str_var.get(), building)

    submit_button = make_button(
        building_department_frame, text="Submit", command=proceed)
    root.bind("<Return>", lambda event: proceed())
    submit_button.pack(pady=scale(STANDARD_PADY), padx=scale(STANDARD_PADX))


def save_input(first_name: str, last_name: str,
               department: str, building: str) -> None:
    """
    Save the user's input (name, building, department) to a text file
    and performs a system action.

    The function appends the provided user input, along with the current
    timestamp, to a file. It also executes a system command and then quits the
    program.

    Args:
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        building (str): The selected building.
        department (str): The selected department.

    Returns:
        None: This function does not return a value.
    """
    current_time = strftime("%Y-%m-%d %H:%M:%S")
    command = f'/usr/bin/say "{first_name} {last_name}"'
    # command = (
    #     f'sudo /usr/bin/jamf recon -realname "{first_name} {last_name}"'
    #     f' -building "{building}"'
    #     # f' -department {DEPARTMENTS[department]}'
    # )

    # jamf command:
    # /usr/local/bin/jamf recon [flags]
    # -realname [str]     '-realname "[first name] [last name]"'
    # -email [str]        '-email [unityID]@ncsu.edu'
    # -building [str]     '-building [SOMETHING Hall]'
    # -room [str]         '-room NCSU-[buidling]-####'
    # -department [str]   '-department NCSU-COS-[department]'

    formatted_information = (
        f"{current_time} - {first_name} {last_name}"
        f" - {building} - {DEPARTMENTS[department]} ({department})\n"
    )

    with open("info_log.txt", "a", encoding="utf-8") as f:
        f.write(formatted_information)

    subprocess.run(["bash", "-c", command], check=False)
    root.destroy()


# Main window
root = ctk.CTk()
root.title("Acknowledgement")
root.attributes('-fullscreen', True)
# root.overrideredirect(True)
root.protocol("WM_DELETE_WINDOW", lambda: None)

background = load_background(root, BACKGROUND_PATH)
background_label = ctk.CTkLabel(root, text="", image=background)
background_label.place(x=0, y=0)

banner_image = load_banner(BANNER_PATH)
banner_label = ctk.CTkLabel(root, text="", image=banner_image)
banner_label.place(x=0, y=0)

# Initial Page
frame = ctk.CTkFrame(root)
frame.pack(expand=True)

ctk.CTkLabel(frame, text=ACKNOWLEDGE_MESSAGE,
             font=get_font(LARGER_FONT_SIZE, True),
             pady=scale(STANDARD_PADY * 5), padx=scale(STANDARD_PADX * 2.5),
             fg_color=REYNOLDS_RED).pack(expand=True)

acknowledge_button = make_button(
    frame, text="Next", command=name_input_page)
acknowledge_button.pack(pady=scale(STANDARD_PADX // 2))

root.mainloop()
