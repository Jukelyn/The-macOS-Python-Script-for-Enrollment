"""
This module provides a graphical user interface for gathering user input
regarding their name, building, and department for workstation enrollment.

The program is built using the Tkinter library and displays a series of pages:

1. **Acknowledgement Page**: A message asking the user to acknowledge and
proceed with the input process.

2. **Name Input Page**: Prompts the user to enter their first and last names.

3. **Building and Department Selection Page**: Allows the user to select their
building and department from predefined dropdown options.

4. **Save and Submit**: After gathering the necessary information, the data is
saved into a text file.

Key functionalities:
- The GUI elements (labels, entry fields, dropdowns, buttons) are dynamically
scaled based on a scaling factor for better accessibility.
- Data is saved in a text file with a timestamp and the user's input.
- The application is intended for use on macOS.

The module also includes helper functions for refreshing the window, clearing
widgets, and centering the window on the screen.

Dependencies:
- Tkinter for GUI components.
- strftime and subprocess for handling time formatting and executing system
commands.
- Callable for typehinting

"""
import tkinter as tk
from time import strftime
import subprocess
from typing import Callable

SCALING_FACTOR = 1.5  # Scale everything by 2.5


def scale(value):
    """
    Scales the given value by a predefined scaling factor.

    This function multiplies the input value by the constant scaling factor
    (SCALING_FACTOR) and returns the result as an integer. It's used for
    adjusting sizes and positions dynamically based on screen resolution.

    Args:
        value (float): The value to be scaled.

    Returns:
        int: The scaled value, rounded to the nearest integer.
    """
    return int(value * SCALING_FACTOR)


def center_window(window, width: int, height: int):
    """
    Centers the provided window on the screen.

    This function calculates the appropriate position to place the window in
    the center of the screen based on the screen's resolution and the window's
    dimensions.

    Args:
        window (tk.Tk): The window object to be centered.
        width (int): The desired width of the window.
        height (int): The desired height of the window.

    Returns:
        None: This function modifies the window's position but does not return
            a value.
    """

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def refresh_window() -> None:
    """
    Forces the root window to refresh and redraw its contents.

    This function is used to ensure that any changes made to the window or
    its widgets are immediately reflected on the screen. It triggers the
    internal update processes of the window.

    Returns:
        None: This function performs window updates but does not return a
            value.
    """
    root.update_idletasks()
    root.update()


def clear_root() -> None:
    """
    Clears all widgets from the root window.

    This function iterates through all child widgets of the root window and
    destroys them, effectively clearing the window. After clearing the widgets,
    it refreshes the window to update the display.

    Returns:
        None: This function modifies the root window but does not return a
            value.
    """
    for widget in root.winfo_children():
        widget.destroy()
    refresh_window()


def get_name_label(working_frame: tk.Frame, name_part: str) -> tk.Label:
    """
    Creates and returns a label widget for the user's name input.

    Args:
        working_frame (tk.Frame): The parent frame where the label will be
        placed.
        name_part (str): The part of the name. Defaults to "".

    Returns:
        tk.Label: A Label widget displaying the appropriate name prompt.
    """
    text = f"{name_part} Name:"
    label = tk.Label(working_frame, text=text, font=("Arial", scale(10)))

    return label


def grid_position(current_widget: tk.Widget, row: int, col: int):
    """
    Helper function for placing widgets in a grid layout with scaling and
    padding.

    Args:
        current_widget (tk.Widget): The widget (Label, Entry, etc.) to be
            placed in the grid.
        row (int): The row position for the widget.
        col (int): The column position for the widget.

    Returns:
        None: The function places the widget in the grid and does not return a
        value.
    """
    sticky = "e" if isinstance(current_widget, tk.Label) else ""

    return current_widget.grid(row=row, column=col, padx=scale(10),
                               pady=scale(5), sticky=sticky)


def get_entry_field(current_frame: tk.Frame) -> tk.Entry:
    """
    Creates and returns an entry field widget for user input.

    Args:
        current_frame (tk.Frame): The parent frame where the entry field will
        be placed.

    Returns:
        tk.Entry: An Entry widget allowing the user to input text.
    """
    return tk.Entry(current_frame, font=("Arial", scale(10)))


def make_button(current_frame: tk.Frame, text: str,
                command: Callable[[], None]) -> tk.Button:
    """
    Creates a button widget and adds it to the specified frame.

    Args:
        current_frame (tk.Frame): The parent frame where the button will
            be placed.
        text (str): The label text to display on the button.
        command (Callable[[], None]): The function to call when the
            button is clicked.

    Returns:
        tk.Button: A button widget configured with the specified properties.
    """
    return tk.Button(current_frame, text=text, font=("Arial", scale(10)),
                     command=command)


def name_input_page() -> None:
    """
    Displays the page for entering the user's first and last name, and handles
    navigation to the next page.

    Clears the root window and creates a new frame with fields for the user to
    input their first and last name. Once both names are entered, the user can
    click the 'Next' button to proceed to the building and department selection
    page.

    Returns:
        None: This function does not return any value.
    """
    clear_root()  # Clear existing widgets

    name_input_frame = tk.Frame(root)
    name_input_frame.pack(expand=True)

    first_name = get_name_label(name_input_frame, "First")
    grid_position(first_name, 0, 0)

    first_name_entry = get_entry_field(name_input_frame)
    grid_position(first_name_entry, 0, 1)

    last_name = get_name_label(name_input_frame, "Last")
    grid_position(last_name, 1, 0)

    last_name_entry = get_entry_field(name_input_frame)
    grid_position(last_name_entry, 1, 1)

    def proceed():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        if first_name and last_name:
            building_department_input(first_name, last_name)

    name_button = make_button(name_input_frame, text="Next", command=proceed)
    name_button.grid(row=2, columnspan=2, pady=scale(10))

    root.bind("<Return>", lambda event: proceed())


def get_selection_label(current_frame: tk.Frame, selection: str) -> tk.Label:
    """
    Creates and returns a label widget prompting the user to select an option.

    Args:
        current_frame (tk.Frame): The parent frame where the label will be
            placed.
        selection (str): The specific selection prompt. Defaults to "".

    Returns:
        tk.Label: A label widget with the formatted selection prompt.
    """
    text = f"Select your {selection}:"

    label = tk.Label(current_frame, text=text,
                     font=("Arial", scale(10)))
    label.pack(pady=scale(10), padx=scale(20))

    return label


def get_dropdown(current_frame: tk.Frame, options: list[str]) -> tk.StringVar:
    """
    Creates a dropdown menu with a list of options and returns the variable
    holding the selected option.

    Args:
        current_frame (tk.Frame): The parent frame where the dropdown will be
            placed.
        options (list[str]): A list of options to be displayed in the dropdown
            menu.

    Returns:
        tk.StringVar: A StringVar that holds the selected option from the
            dropdown.
    """
    dropdown_str_var = tk.StringVar(current_frame)
    dropdown_str_var.set(options[0])  # Default to the first option
    dropdown = tk.OptionMenu(current_frame, dropdown_str_var, *options)
    dropdown.pack(pady=scale(10), padx=scale(20))

    # Adjust dropdown font size (selected)
    dropdown.config(font=("Arial", scale(10)))

    # Adjust dropdown font size (non-selected)
    dropdown["menu"].config(font=("Arial", scale(7)))

    return dropdown_str_var


def building_department_input(first_name: str, last_name: str):
    """
    Displays the page for selecting the building and department,
    and handles saving the selections.

    Clears the root window and creates a new frame with dropdown menus for
    selecting the building and department. Once both selections are made, the
    user can click the 'Submit' button to save the input and proceed.

    Args:
        first_name (str): The user's first name.
        last_name (str): The user's last name.

    Returns:
        None: This function does not return any value.
    """
    clear_root()  # Clear existing widgets

    building_department_frame = tk.Frame(root)
    building_department_frame.pack(expand=True)

    # Building Label
    get_selection_label(building_department_frame, "building")

    # Building Dropdown
    buildings = ["SAS Hall", "Thomas Hall", "Ricks Hall"]
    # This creates the dropdown
    building_str_var = get_dropdown(building_department_frame, buildings)

    # Department Label
    get_selection_label(building_department_frame, "department")

    # Department Dropdown
    departments = ["Math", "Biology", "Chemistry", "Physics"]
    # This creates the dropdown
    department_str_var = get_dropdown(building_department_frame, departments)

    # Submit Button
    def proceed():
        building = building_str_var.get()
        department = department_str_var.get()
        save_input(first_name, last_name, building, department)

    submit_button = make_button(building_department_frame, text="Submit",
                                command=proceed)
    root.bind("<Return>", lambda event: proceed())
    submit_button.pack(pady=scale(10), padx=scale(20))


def save_input(first_name: str, last_name: str,
               building: str, department: str) -> None:
    """
    Saves the user's input (name, building, department) to a text file
    and performs a system action.

    The function appends the user's information along with the current
    timestamp to a file. It also executes a system command to speak the user's
    name and then exits the application.

    Args:
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        building (str): The building selected by the user.
        department (str): The department selected by the user.

    Returns:
        None: This function does not return any value.
    """
    current_time = strftime("%Y-%m-%d %H:%M:%S")
    formatted_information = f"{current_time} - {first_name} \
{last_name} - {building} - {department}\n"

    with open("user_input.txt", "a", encoding="utf-8") as f:
        f.write(formatted_information)

    bash_command = f"/usr/bin/say {first_name} {last_name}"
    subprocess.run(["bash", "-c", bash_command], check=False)
    root.quit()


# Main window
root = tk.Tk()
root.title("Acknowledgement")
root.attributes('-fullscreen', True)
root.protocol("WM_DELETE_WINDOW", lambda: None)  # Prevent closing
center_window(root, scale(600), scale(150))

# Initial Page
frame = tk.Frame(root)
frame.pack(expand=True)

ACKNOWLEDGE_MESSAGE = "Please answer a few quick questions to get \
this workstation properly enrolled with management."

tk.Label(frame, text=ACKNOWLEDGE_MESSAGE, font=(
    "Arial", scale(10))).pack(pady=scale(20))
acknowledge_button = make_button(frame, text="Acknowledge & Next",
                                 command=name_input_page)
acknowledge_button.pack(pady=scale(10))

root.mainloop()
