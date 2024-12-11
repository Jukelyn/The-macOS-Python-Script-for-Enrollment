![License](https://img.shields.io/badge/License-CC%20BY%20NC%20ND%204.0-lightgrey)

This script provides a graphical user interface for gathering user input
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

The script also includes helper functions for refreshing the window, clearing
widgets, and centering the window on the screen.

Dependencies:
- Tkinter for GUI components.
- strftime and subprocess for handling time formatting and executing system
commands.
- Callable for typehinting


This script requires Python v3.9 or higher.