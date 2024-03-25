import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Progressbar
from tkinter.filedialog import askdirectory
from tkinter import filedialog
import csv
import pandas as pd
from PIL import Image, ImageTk
import os
import glob
import datetime
import shutil
from datetime import datetime
from tempfile import NamedTemporaryFile
import interface
import common
import sys

active_csv_file = None

documentspath = os.path.expanduser('~/Documents')
directory = 'AutoDKP by Pie123'
parent_dir = documentspath
folderpath = os.path.join(parent_dir, directory)
if not os.path.exists(folderpath):
    os.mkdir(folderpath)
    print("Directory '% s' created" % directory)

# Create subfolders
login_info_path = os.path.join(folderpath, "Login info")  # New subfolder path
active_csv_path = os.path.join(folderpath, "Active CSV files")
archive_csv_path = os.path.join(folderpath, "Archive and Backup CSV files")
archived_log_path = os.path.join(folderpath, "Archived Log Files")  # New subfolder path
nickname_csv_path = os.path.join(folderpath, "Nickname CSV")
for path in [active_csv_path, archive_csv_path, archived_log_path,
             login_info_path, nickname_csv_path]:  # Include new subfolder path in the loop
    if not os.path.exists(path):
        os.mkdir(path)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def archive_active_csvs():
    # Paths to your folders
    active_csv_path = os.path.join(folderpath, "Active CSV files")
    archive_csv_path = os.path.join(folderpath, "Archive and Backup CSV files")

    # Find all CSV files in the active folder
    for csv_file in glob.glob(os.path.join(active_csv_path, "*.csv")):
        # Construct the destination path
        dest_file = os.path.join(archive_csv_path, os.path.basename(csv_file))
        # Move the file
        shutil.move(csv_file, dest_file)
        print(f"Archived: {os.path.basename(csv_file)}")


def load_login_info():
    login_file_path = os.path.join(login_info_path, "webdkp_login_info.csv")
    login_attempted = False
    if os.path.exists(login_file_path):
        with open(login_file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:  # Assuming there's only one row of login info
                # Set URL and directly infer server and clan from it
                common.url = row.get("WebDKP URL", "")
                server, clan = parse_url_details(common.url)
                common.server = server
                common.clan = clan

                # Update remaining fields
                common.username = row.get("Username", "")
                common.password = row.get("Password", "")
                table_name = row.get("Table Name", "")
                common.table_name = table_name
                table_id = row.get("Table ID", "")

                # Update table_ids to be a dictionary mapping names to IDs
                if table_name and table_id:
                    # Assuming table_id is a single integer ID for the corresponding table_name
                    common.table_ids = {table_name: int(table_id)}

                # Attempt login and sync if login details are present
                if common.username and common.password:
                    interface.login()
                    interface.sync_players()
                    login_attempted = True
                    print("Logged in successfully.")
                break  # Assuming only one set of login details

    if not login_attempted:
        print("Login info file does not exist or is incomplete. Please enter your login details.")
        # Reset variables to defaults if the login wasn't attempted/succeeded
        reset_common_defaults()

    return login_attempted


def parse_url_details(url):
    """
    Extracts the server and clan name from the given WebDKP URL.
    Example URL: https://www.webdkp.com/dkp/Unknown/MythicLegends/
    """
    parts = url.split('/')
    try:
        # The server and clan are expected to be the 5th and 6th parts of the URL, respectively
        server = parts[4]
        clan = parts[5]
        return server, clan
    except IndexError:
        return "", ""  # Return empty strings if URL is not in the expected format


def reset_common_defaults():
    common.url = ""
    common.username = ""
    common.password = ""
    common.clan = ""
    common.server = ""
    common.table_ids = {}


archive_active_csvs()

load_login_info()

# Global variable to keep track of current image index and the list of image paths
image_index = 0
image_paths = []
selected_boss = ""
input_dir = ""


def open_new_window():
    newWindow = tk.Toplevel(root)

    # creating 26x7 grid
    for i in range(7):
        for j in range(22):
            newWindow.grid_columnconfigure(i, weight=1, uniform="foo")
            newWindow.grid_rowconfigure(j, weight=1, uniform="foo")

    # Load the CSV file

    # Load the CSV file
    df = pd.read_csv(resource_path('yourfile.csv'))

    # Placing text and text boxes
    tk.Label(newWindow, text="DL", width=20).grid(row=0, column=0, columnspan=2)
    tk.Label(newWindow, text="EDL", width=20).grid(row=0, column=2, columnspan=2)
    tk.Label(newWindow, text="Legacy", width=20).grid(row=0, column=4, columnspan=2)
    tk.Label(newWindow, text="World Bosses", width=20).grid(row=4, column=4, columnspan=2)
    tk.Label(newWindow, text="Ring Boss", width=20).grid(row=15, column=4, columnspan=2)

    tk.Label(newWindow, text="Boss").grid(row=1, column=0)
    tk.Label(newWindow, text="DKP Value").grid(row=1, column=1)
    tk.Label(newWindow, text="Boss").grid(row=1, column=2)
    tk.Label(newWindow, text="DKP Value").grid(row=1, column=3)
    tk.Label(newWindow, text="Boss").grid(row=1, column=4)
    tk.Label(newWindow, text="DKP Value").grid(row=1, column=5)
    tk.Label(newWindow, text="Boss").grid(row=5, column=4)
    tk.Label(newWindow, text="DKP Value").grid(row=5, column=5)
    tk.Label(newWindow, text="Boss").grid(row=16, column=4)
    tk.Label(newWindow, text="DKP Value").grid(row=16, column=5)

    # Define a list of bosses
    bosses = ["155/4", "155/5", "155/6", "160/4", "160/5", "160/6", "165/4", "165/5", "165/6", "170/4", "170/5",
              "170/6", "180/4", "180/5", "180/6", "185/4", "185/5", "185/6", "190/4", "190/5", "190/6", "195/4",
              "195/5", "195/6", "200/4", "200/5", "200/6", "205/4", "205/5", "205/6", "210/4", "210/5", "210/6",
              "215/4", "215/5", "215/6", "5*", "6*", "Aggy", "Hrung", "Mord", "Necro", "Prot Base", "Prot Prime",
              "Gele", "BT", "Dino", "5* RB", "6* RB"]
    boss_labels = []
    boss_values = []

    for i, boss in enumerate(bosses):
        boss_value_str = df.loc[df["Boss"] == boss, "DKP Value"].values[0] if boss in df["Boss"].values else ""

        # Determine grid position
        if i < 35:  # Existing bosses
            row = i + 2 if i < 15 else i - 13
            column = 0 if i < 15 else 2
        elif 36 <= i < 38:  # Legacy bosses
            row = i - 34  # Updated position for Legacy bosses
            column = 4  # Updated position for Legacy bosses
        elif 38 <= i <= 46:  # World Bosses
            row = i - 32  # Updated position for World Bosses
            column = 4  # Updated position for World Bosses
        elif i > 46:
            row = i - 30  # Updated position for Ring Bosses
            column = 4

        boss_label = tk.Label(newWindow, text=boss)
        boss_label.grid(row=row, column=column, sticky='n')

        boss_value = tk.Entry(newWindow)
        boss_value.insert(0, boss_value_str)  # Automatically fill the value
        boss_value.grid(row=row, column=column + 1, sticky='n')

        boss_labels.append(boss_label)
        boss_values.append(boss_value)

    def update_values():
        # Open the CSV file and append the data
        with open(resource_path('yourfile.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Boss", "DKP Value"])
            for boss_label, boss_value in zip(boss_labels, boss_values):
                writer.writerow([boss_label.cget("text"), boss_value.get()])
        print("Values Updated")

    ttk.Button(newWindow, text="Update Values", command=update_values).grid(row=2, column=7)


def get_selected_boss():
    return bosses[chkValue.get()]


def display_dkp_value():
    df = pd.read_csv(resource_path('yourfile.csv'))
    boss_names = ["155/4", "155/5", "155/6", "160/4", "160/5", "160/6", "165/4", "165/5", "165/6", "170/4", "170/5",
                  "170/6", "180/4", "180/5", "180/6", "185/4", "185/5", "185/6", "190/4", "190/5", "190/6", "195/4",
                  "195/5", "195/6", "200/4", "200/5", "200/6", "205/4", "205/5", "205/6", "210/4", "210/5", "210/6",
                  "215/4", "215/5", "215/6", "5*", "6*", "Aggy", "Hrung", "Mord", "Necro", "Prot Base", "Prot Prime",
                  "Gele", "BT", "Dino", "5* RB", "6* RB"]
    selected_boss = boss_names[chkValue.get()]
    dkp_value = df.loc[df["Boss"] == selected_boss, "DKP Value"].values[0]
    dkp_value_label.config(text=str(dkp_value))


root = tk.Tk()
root.title("Python GUI")

# creating 22x7 grid
for i in range(7):
    for j in range(25):
        root.grid_columnconfigure(i, weight=1, uniform="foo")
        root.grid_rowconfigure(j, weight=1, uniform="foo", minsize=10)

# Label for "Name of Poster"
tk.Label(root, text="Name of Poster", width=20).grid(row=2, column=0, columnspan=2)

# Text box for Name of Poster, set width to fill the columns
name_of_poster = tk.Entry(root, width=35)
name_of_poster.grid(row=3, column=0, columnspan=2)

# Place image at 0,4 with columnspan of 6 and rowspan of 4
# Note: Replace 'image_path.png' with the path to your image
image = Image.open(resource_path('egg.png'))

# Resize the image to fit the GUI
max_height = 400
max_width = 600
image.thumbnail((max_width, max_height))

photo = ImageTk.PhotoImage(image)

image_label = tk.Label(root, image=photo, height=max_height)
image_label.grid(row=0, column=4, columnspan=6, rowspan=20)

# Global list to keep track of entry widgets for names and nicknames
entry_widgets = []


# Function to open the settings window
def open_settings_window():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x100")  # Set the window size (adjust as needed)

    # Move the button to change DKP Value to the new window
    change_dkp_button = ttk.Button(settings_window, text="change DKP Value", command=open_new_window)
    change_dkp_button.grid(row=0, column=0)

    # New button to create Nickname set
    create_nickname_button = ttk.Button(settings_window, text="Create Nickname set", command=open_nickname_set_creation)
    create_nickname_button.grid(row=1, column=0)


def open_nickname_set_creation():
    nickname_window = tk.Toplevel(root)
    nickname_window.title("Create Nickname Set")

    # Labels
    tk.Label(nickname_window, text="Name (Case Sensitive)").grid(row=0, column=0)
    tk.Label(nickname_window, text="Nicknames (separate by a comma and space)").grid(row=0, column=1)

    # Initialize the list to hold the entry widgets
    entries_list = []

    def add_row():
        row_index = len(entries_list) + 1
        name_entry = tk.Entry(nickname_window)
        nickname_entry = tk.Entry(nickname_window)
        name_entry.grid(row=row_index, column=0)
        nickname_entry.grid(row=row_index, column=1)
        entries_list.append((name_entry, nickname_entry))

        # Move the buttons down
        add_row_button.grid(row=row_index + 1)
        remove_row_button.grid(row=row_index + 1, column=1)

        # Adjust window size dynamically
        nickname_window.geometry('')

    def remove_row():
        if entries_list:
            name_entry, nickname_entry = entries_list.pop()
            name_entry.destroy()
            nickname_entry.destroy()

            row_index = len(entries_list) + 1
            add_row_button.grid(row=row_index + 1)
            remove_row_button.grid(row=row_index + 1, column=1)

            # Adjust window size dynamically
            nickname_window.geometry('')

    def save_to_csv():
        # Ensure the folder exists
        if not os.path.exists(nickname_csv_path):
            os.makedirs(nickname_csv_path)

        csv_file_path = os.path.join(nickname_csv_path, 'nicknames.csv')
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write the header
            writer.writerow(['Name', 'Nicknames'])
            # Write the entries
            for name_entry, nickname_entry in entries_list:
                writer.writerow([name_entry.get(), nickname_entry.get()])

    # Add Row button
    add_row_button = ttk.Button(nickname_window, text="Add Row", command=add_row)
    add_row_button.grid(row=1, column=0)

    # Remove Row button
    remove_row_button = ttk.Button(nickname_window, text="Remove Row", command=remove_row)
    remove_row_button.grid(row=1, column=1)

    def load_from_csv():
        csv_file_path = os.path.join(nickname_csv_path, 'nicknames.csv')
        if os.path.exists(csv_file_path):
            with open(csv_file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Add a row for each entry
                    add_row()
                    # Populate the last entry with data from CSV
                    entries_list[-1][0].insert(0, row['Name'])
                    entries_list[-1][1].insert(0, row['Nicknames'])

    load_from_csv()

    nickname_window.protocol("WM_DELETE_WINDOW", lambda: [save_to_csv(), nickname_window.destroy()])


# Create a "Settings" button on the main window
settings_button = ttk.Button(root, text="Settings", command=open_settings_window)
settings_button.grid(row=1, column=1)


def webdkp_login():
    loginWindow = tk.Toplevel(root)
    loginWindow.title("WebDKP Login")

    # Labels
    tk.Label(loginWindow, text="WebDKP url:").grid(row=0, column=0)
    tk.Label(loginWindow, text="Username:").grid(row=1, column=0)
    tk.Label(loginWindow, text="Password:").grid(row=2, column=0)
    tk.Label(loginWindow, text="Table Name").grid(row=3, column=0)
    tk.Label(loginWindow, text="Table ID").grid(row=4, column=0)

    # Textboxes / Entry Widgets
    webdkp_url_entry = tk.Entry(loginWindow)
    webdkp_url_entry.grid(row=0, column=1)
    username_entry = tk.Entry(loginWindow)
    username_entry.grid(row=1, column=1)
    password_entry = tk.Entry(loginWindow, show="*")
    password_entry.grid(row=2, column=1)
    tablename_entry = tk.Entry(loginWindow)
    tablename_entry.grid(row=3, column=1)
    tableid_entry = tk.Entry(loginWindow)
    tableid_entry.grid(row=4, column=1)

    def parse_url_details(url):
        """
        Extracts the server and clan name from the given WebDKP URL.
        Example URL: https://www.webdkp.com/dkp/Unknown/MythicLegends/
        """
        parts = url.split('/')
        if len(parts) > 4:
            server = parts[-3]
            clan = parts[-2]
            return server, clan
        return "", ""

    # Function to populate fields
    def populate_login_fields():
        login_file_path = os.path.join(login_info_path, "webdkp_login_info.csv")
        if os.path.exists(login_file_path):
            with open(login_file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:  # Assuming there's only one row
                    webdkp_url_entry.insert(0, row.get("WebDKP URL", ""))
                    username_entry.insert(0, row.get("Username", ""))
                    password_entry.insert(0, row.get("Password", ""))
                    tablename_entry.insert(0, row.get("Table Name", ""))
                    tableid_entry.insert(0, row.get("Table ID", ""))
                    break  # Assuming only one set of login details

    # Call populate_login_fields when window opens
    populate_login_fields()

    # Checkbox
    save_login_var = tk.BooleanVar(value=True)  # Normally checked
    save_login_check = tk.Checkbutton(loginWindow, text="Save login", variable=save_login_var)
    save_login_check.grid(row=5, column=1)

    def update_login():
        # Get values from entry widgets
        url = webdkp_url_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        table_name = tablename_entry.get()
        common.table_name = table_name
        table_id = tableid_entry.get()
        save_login = save_login_var.get()

        # Parse server and clan name from URL
        server, clan_name = parse_url_details(url)

        # Proceed to save if Save login is checked
        if save_login:
            login_file_path = os.path.join(login_info_path, "webdkp_login_info.csv")
            with open(login_file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                # Notice the adjusted headers according to the provided fields
                writer.writerow(["WebDKP URL", "Username", "Password", "Table Name", "Table ID"])
                writer.writerow([url, username, password, table_name, table_id])
            print(f"Login information saved to {login_file_path}")

    # Button
    update_login_button = tk.Button(loginWindow, text="update login")
    update_login_button.grid(row=5, column=0)
    update_login_button.config(command=update_login)

    def on_close():
        if not load_login_info():  # Attempt to login upon window close if not done at startup
            print("Login details are missing or incorrect. Unable to log in.")
        loginWindow.destroy()  # Explicitly close the window

    loginWindow.protocol("WM_DELETE_WINDOW", on_close)


# Assuming root is your Tk() main window
# root = tk.Tk()
# root.mainloop()


# Create a "WebDKP Login" button on the main window
webdkp_login_button = ttk.Button(root, text="WebDKP Login", command=webdkp_login)
webdkp_login_button.grid(row=1, column=2)


def open_add_players_window():
    add_players_window = tk.Toplevel(root)
    add_players_window.title("Add Players to WebDKP")

    # Label for player names entry
    tk.Label(add_players_window, text="Player Names (separate by comma and space)").grid(row=0, column=0, columnspan=3)

    # Entry widget for player names
    player_names_entry = tk.Entry(add_players_window)
    player_names_entry.grid(row=1, column=0, columnspan=2, sticky="ew")

    # Options menu for player class
    player_class_var = tk.StringVar(add_players_window)
    player_class_var.set("Druid")  # default value
    player_class_options = ["Druid", "Mage", "Rogue", "Warrior", "Hunter"]
    player_class_menu = tk.OptionMenu(add_players_window, player_class_var, *player_class_options)
    player_class_menu.grid(row=1, column=2)

    # Checkbox for automatic addition on window close
    auto_add_var = tk.BooleanVar(value=False)  # Default unchecked
    auto_add_checkbox = tk.Checkbutton(add_players_window, text="Automatically add players on window close",
                                       variable=auto_add_var)
    auto_add_checkbox.grid(row=2, column=0, columnspan=3, sticky="w")

    # Button to add players
    add_players_button = ttk.Button(add_players_window, text="Add Players",
                                    command=lambda: add_players_interface(player_names_entry.get(),
                                                                          player_class_var.get()))
    add_players_button.grid(row=3, column=0, columnspan=3)

    # Handle window close
    def on_window_close():
        if auto_add_var.get():
            add_players_interface(player_names_entry.get(), player_class_var.get())
        add_players_window.destroy()

    add_players_window.protocol("WM_DELETE_WINDOW", on_window_close)


def add_players_interface(player_names_str, player_class):
    if not player_names_str.strip():  # Ignore if empty
        return

    for player_name in player_names_str.split(","):
        player_name = player_name.strip()
        if player_name:  # Check if the player name is not empty after stripping
            print(f"Adding Player: {player_name} as a {player_class}")  # Debug: Confirm the action
            interface.addPlayer(player_name, player_class)  # Call the interface function to add the player

    # Note: This assumes all players being added are of the same class. Adjust as needed.


add_players_button = ttk.Button(root, text="Add Players to WebDKP", command=open_add_players_window)
add_players_button.grid(row=1, column=3)


def open_screenshots_folder():
    global image_index
    global image_paths
    global active_csv_file

    input_dir = askdirectory(title='Select Folder')
    image_paths = glob.glob(os.path.join(input_dir, '*.png')) + glob.glob(os.path.join(input_dir, '*.jpg'))

    # Get filenames from selected folder
    filenames = [os.path.basename(path) for path in image_paths]

    # Function to find and move matching CSV
    def find_and_move_csv(folder_path):
        for csv_file in glob.glob(os.path.join(folder_path, '*.csv')):
            with open(csv_file, 'r') as file:
                reader = csv.reader(file)
                csv_filenames = [row[0] for row in list(reader)[1:]]  # Skip header
            if set(csv_filenames) == set(filenames):  # Move this condition outside the 'with' block
                new_path = os.path.join(active_csv_path, os.path.basename(csv_file))
                shutil.move(csv_file, new_path)  # Move to Active folder
                return new_path
        return None

    # Search Active and Archive folders for matching CSV
    active_csv_file = find_and_move_csv(active_csv_path) or find_and_move_csv(archive_csv_path)

    # If no matching CSV found, create new one
    if not active_csv_file:
        timestamp = datetime.now().strftime("%m.%d.%Y-%H.%M.%S")
        csv_name = f"CSV-AUTODKP-{timestamp}.csv"
        active_csv_file = os.path.join(active_csv_path, csv_name)
        with open(active_csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                ['Filename', 'Poster Awarded', 'Players Awarded', 'DKP Awarded', 'Boss', 'Awarded?'])  # Write header
            writer.writerows([(name, '', '', '') for name in filenames])  # Write filenames

    print(f"Active CSV file set for folder: {input_dir}")
    print(f"active_csv_file: {active_csv_file}")

    if image_paths:
        image_index = 0
        load_image(image_paths[image_index])


def update_text_boxes(filename):
    global active_csv_file
    with open(active_csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == os.path.basename(filename):
                poster_awarded_textbox.delete(0, tk.END)
                poster_awarded_textbox.insert(0, row[1])
                players_awarded_textbox.delete(0, tk.END)
                players_awarded_textbox.insert(0, row[2])
                dkp_value_textbox.delete(0, tk.END)
                dkp_value_textbox.insert(0, row[3])
                # Update the selected boss radio button if needed
                selected_boss_index = bosses.index(row[4])  # Assuming row[4] contains the boss name
                chkValue.set(selected_boss_index)
                break  # No need for the second break


def update_csv(filename, poster_awarded, players_awarded, dkp_awarded):
    global active_csv_file
    boss_name = get_selected_boss()  # Fetch the currently selected boss name
    temp_file = NamedTemporaryFile(mode='w', newline='', delete=False)
    with open(active_csv_file, 'r') as csv_file, temp_file:
        reader = csv.reader(csv_file)
        writer = csv.writer(temp_file)
        for row in reader:
            if row[0] == filename:
                # Assuming the boss's name should be included after the dkp_awarded
                writer.writerow([filename, poster_awarded, players_awarded, dkp_awarded, boss_name])
            else:
                writer.writerow(row)
    shutil.move(temp_file.name, active_csv_file)


def load_image(image_path):
    global photo
    global image_label
    image = Image.open(image_path)
    max_height = 600
    max_width = 800
    image.thumbnail((max_width, max_height))
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo  # Keep reference to prevent GC

    # Calculate progress
    progress_fraction = (image_index + 1) / len(image_paths)
    progress_percentage = progress_fraction * 100

    # Update the progress bar
    progress_bar['value'] = progress_percentage
    progress_label['text'] = f'{image_index + 1}/{len(image_paths)} ({progress_percentage:.2f}%)'

    update_text_boxes(os.path.basename(image_path))
    # Read the CSV and find the corresponding value for the current image
    df = pd.read_csv(active_csv_file)
    poster_awarded = df.loc[df["Filename"] == os.path.basename(image_path), "Poster Awarded"].values[0]

    # Update the poster awarded text box, but avoid autofilling "nan"
    poster_awarded_textbox.delete(0, tk.END)
    name_of_poster.delete(0, tk.END)  # Clear name_of_poster text box
    if pd.notna(poster_awarded):  # Check if the value is not NaN
        poster_awarded_textbox.insert(0, str(poster_awarded))
        name_of_poster.insert(0, str(poster_awarded))  # Mirror the value to name_of_poster


button_open_screenshots = ttk.Button(root, text="Open Screenshots folder", command=open_screenshots_folder)
button_open_screenshots.grid(row=1, column=0)


def update_dkp_value_textbox():
    df = pd.read_csv(resource_path('yourfile.csv'))
    selected_boss = bosses[chkValue.get()]
    dkp_value = df.loc[df["Boss"] == selected_boss, "DKP Value"].values[0]
    dkp_value_textbox.delete(0, tk.END)  # Remove the current text
    dkp_value_textbox.insert(0, str(dkp_value))  # Insert the new value

    # Update the CSV with the new values
    update_csv(os.path.basename(image_paths[image_index]), poster_awarded_textbox.get(), players_awarded_textbox.get(),
               dkp_value_textbox.get())


def mirror_content(entry1, entry2):
    content = entry1.get()
    entry2.delete(0, tk.END)
    entry2.insert(0, content)


# Placing radio buttons
bosses = ["155/4", "155/5", "155/6", "160/4", "160/5", "160/6", "165/4", "165/5", "165/6", "170/4", "170/5", "170/6",
          "180/4", "180/5", "180/6", "185/4", "185/5", "185/6", "190/4", "190/5", "190/6", "195/4", "195/5", "195/6",
          "200/4", "200/5", "200/6", "205/4", "205/5", "205/6", "210/4", "210/5", "210/6", "215/4", "215/5", "215/6",
          "5*", "6*", "Aggy", "Hrung", "Mord", "Necro", "Prot Base", "Prot Prime", "Gele", "BT", "Dino", "5* RB",
          "6* RB"]
chkValue = tk.IntVar()

# new text
tk.Label(root, text="DL").grid(row=4, column=0)  # moved down 4 rows
tk.Label(root, text="EDL").grid(row=4, column=1)  # moved down 4 rows
tk.Label(root, text="Legacy").grid(row=4, column=2)  # moved down 4 rows
tk.Label(root, text="World Bosses").grid(row=7, column=2)  # moved down 4 rows
tk.Label(root, text="Ring Bosses").grid(row=17, column=2)  # moved down 4 rows

for i, boss in enumerate(bosses):
    chkInstance = ttk.Radiobutton(root, text=boss, variable=chkValue, value=i, command=update_dkp_value_textbox)
    if i < 35:
        chkInstance.grid(row=i + 5 if i < 15 else i - 14 + 4, column=0 if i < 15 else 1)  # moved down 4 rows
    elif 35 < i < 38:  # For indices 36 and 37 (i.e., "5*", "6*")
        chkInstance.grid(row=5 + i - 36, column=2, sticky='w')  # moved down 4 rows
    elif 37 < i < 47:  # For indices 38 and above (i.e., "Aggy", "Hrung")
        chkInstance.grid(row=5 + i - 35, column=2, sticky='w')  # moved down 4 rows
    elif i >= 47:
        chkInstance.grid(row=5 + i - 34, column=2, sticky='w')  # moved down 4 rows


def update_boss_selection_from_csv(filename):
    df = pd.read_csv(active_csv_file)
    print(df.columns)  # Debugging print to check DataFrame structure
    # Assuming 'Filename' column stores the image filenames and 'Boss' the selected boss
    boss_row = df[df['Filename'] == filename]
    if not boss_row.empty:
        boss_name = boss_row.iloc[0]['Boss']
        if boss_name in bosses:
            boss_index = bosses.index(boss_name)
            chkValue.set(boss_index)
        else:
            chkValue.set(-1)  # Reset if boss not found
    else:
        chkValue.set(-1)  # Reset if filename not found


def next_image():
    global image_index
    update_csv(os.path.basename(image_paths[image_index]), poster_awarded_textbox.get(), players_awarded_textbox.get(),
               dkp_value_textbox.get())
    if image_paths and image_index < len(image_paths) - 1:
        image_index += 1
        load_image(image_paths[image_index])
        chkValue.set(-1)  # Clear the selection of radio buttons
    # Update the button state
    update_boss_selection_from_csv(os.path.basename(image_paths[image_index]))


def previous_image():
    global image_index
    update_csv(os.path.basename(image_paths[image_index]), poster_awarded_textbox.get(), players_awarded_textbox.get(),
               dkp_value_textbox.get())
    if image_paths and image_index > 0:
        image_index -= 1
        load_image(image_paths[image_index])
        chkValue.set(-1)  # Clear the selection of radio buttons
    # Update the button state
    update_boss_selection_from_csv(os.path.basename(image_paths[image_index]))


# Button for next image
next_image_button = ttk.Button(root, text="Next Image >", command=next_image, width=50)
next_image_button.grid(row=21, column=7, columnspan=3, sticky='w')

# Button for previous image
previous_image_button = ttk.Button(root, text="< Previous Image", command=previous_image, width=50)
previous_image_button.grid(row=21, column=4, columnspan=3, sticky='e')

# Left button with "< Previous Image" functionality
left_previous_image_button = ttk.Button(root, text="< Previous Image", command=previous_image, width=20)
left_previous_image_button.grid(row=3, column=2, sticky='e')

# Right button with "Next Image >" functionality
right_next_image_button = ttk.Button(root, text="Next Image >", command=next_image, width=20)
right_next_image_button.grid(row=3, column=3, sticky='w')


def on_dkp_value_textbox_lose_focus(event):
    update_csv(os.path.basename(image_paths[image_index]), players_awarded_textbox.get(), dkp_value_textbox.get())


def on_players_awarded_textbox_lose_focus(event):
    update_csv(os.path.basename(image_paths[image_index]), players_awarded_textbox.get(), dkp_value_textbox.get())


# Label for "DKP Awarded"
tk.Label(root, text="DKP Awarded").grid(row=22, column=8, columnspan=2)

# Text box to show DKP value
dkp_value_textbox = tk.Entry(root, width=40)
dkp_value_textbox.grid(row=23, column=8, columnspan=2, sticky='w')

# Label for "Players awarded"
players_awarded_label = tk.Label(root, text="Players awarded")
players_awarded_label.grid(row=22, column=4, columnspan=3)

# Text box for players awarded
players_awarded_textbox = tk.Entry(root, width=80)
players_awarded_textbox.grid(row=23, column=4, columnspan=3, rowspan=1, sticky='e')

# Label for "Poster awarded"
players_awarded_label = tk.Label(root, text="Poster awarded")
players_awarded_label.grid(row=22, column=7, columnspan=1)

# Text Box for poster awarded
poster_awarded_textbox = ttk.Entry(root)
poster_awarded_textbox.grid(row=23, column=7)

# Create a progress bar
progress_bar = Progressbar(root, orient=tk.HORIZONTAL, length=180, mode='determinate')
progress_bar.grid(row=20, column=4, columnspan=6)

# Create a label to display the fraction and percentage
progress_label = tk.Label(root, text='0/0 (0.00%)')
progress_label.grid(row=20, column=3, columnspan=6)


def set_gui_to_row(row):
    global image_index, image_paths
    filename = row["Filename"]  # Assuming this is the correct key for the filename
    try:
        full_path = os.path.join(input_dir, filename)
        print(f"Looking for {full_path} in image_paths")
        print(image_paths)  # For debugging
        image_index = image_paths.index(full_path)
        load_image(image_paths[image_index])
    except ValueError as e:
        print(f"Error: {e}")
        print(f"Filename {filename} not found in the list.")


def load_nickname_dict():
    nickname_dict = {}
    try:
        with open(os.path.join(nickname_csv_path, "nicknames.csv"), 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                full_name = row["Name"]  # Keep the actual case here
                for nickname in row["Nicknames"].split(", "):
                    # Store the nickname in lowercase but map it to the actual-case full name
                    nickname_dict[nickname.strip().lower()] = full_name
    except FileNotFoundError:
        print("Nickname file not found.")
    return nickname_dict


def translate_nicknames(players_list, nickname_dict):
    # Translate nicknames to full names if in dict, using case-insensitive comparison,
    # but keep the actual case for the full name.
    return [nickname_dict.get(player.strip().lower(), player.strip()) for player in players_list]


def update_dkp():
    global image_paths, image_index
    load_login_info()
    interface.login()
    interface.sync_players()
    df = pd.read_csv(active_csv_file)
    print("Attempting to award DKP for table:", common.table_name)

    # Load nickname mappings
    nickname_dict = load_nickname_dict()

    for index, row in df.iterrows():
        if row.get("Awarded?") != "Yes":
            players_list = [row["Poster Awarded"]] if pd.notna(row["Poster Awarded"]) else []
            if pd.notna(row["Players Awarded"]):
                players_list.extend([player.strip() for player in row["Players Awarded"].split(",") if player.strip()])

            # Translate nicknames to full names
            translated_players_list = translate_nicknames(players_list, nickname_dict)

            if translated_players_list:
                result, message = interface.award_dkp(translated_players_list, row["Boss"], str(row["DKP Awarded"]),
                                                      common.table_name)
                print("Players List=", translated_players_list)  # For debugging
                print("Entire award_dkp message:", translated_players_list, row["Boss"], str(row["DKP Awarded"]),
                      common.table_name)
                if result:
                    df.at[index, "Awarded?"] = "Yes"
                else:
                    tk.messagebox.showerror("Error", f"Failed to award DKP for row {index + 1}: {message}")
                    set_gui_to_row(row)
                    return
            else:
                print(f"No players listed for awarding in row {index + 1}. Skipping.")

    df.to_csv(active_csv_file, index=False)


update_dkp_button = tk.Button(root, text="Update DKP", command=update_dkp, state='normal')
update_dkp_button.grid(row=4, column=3)

# Bind the functions
dkp_value_textbox.bind("<FocusOut>", on_dkp_value_textbox_lose_focus)
players_awarded_textbox.bind("<FocusOut>", on_players_awarded_textbox_lose_focus)

# Assuming name_of_poster_entry and poster_awarded_textbox are the two entry widgets
name_of_poster.bind('<KeyRelease>', lambda event: mirror_content(name_of_poster, poster_awarded_textbox))
poster_awarded_textbox.bind('<KeyRelease>', lambda event: mirror_content(poster_awarded_textbox, name_of_poster))


def on_main_window_close():
    archive_active_csvs()
    root.destroy()  # Or any other cleanup you need to do before closing


root.protocol("WM_DELETE_WINDOW", on_main_window_close)

root.mainloop()
