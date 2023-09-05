import tkinter as tk
import pandas as pd
import os
import gdrive_upload
import os
import datetime
import pytz
import gdrive_sync
selected_item_index = None

def gdrive_sync_bak():
    # Get the last modified time of the Google Drive file as a string
    gdrive_date_str = gdrive_upload.check_date()

    # Convert the string to a datetime object and set it to UTC timezone
    gdrive_date_time = datetime.datetime.fromisoformat(gdrive_date_str).astimezone(pytz.UTC)

    # Specify the filename of the local file you want to check
    filename = 'game_collection.xlsx'

    try:
        # Get the last modified time of the local file and set it to UTC timezone
        local_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(filename), tz=pytz.UTC)

        # Compare the two timestamps
        time_difference = gdrive_date_time - local_modified_time

        if time_difference.total_seconds() > 0:
            print("The Google Drive file is newer than the local file.")
        elif time_difference.total_seconds() < 0:
            print("The local file is newer than the Google Drive file.")
        else:
            print("The files have the same last modified time.")

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def update_entry():
    global selected_item_index
    title = title_entry.get()
    system = system_entry.get()
    genre = genre_entry.get()
    price_charting = float(price_charting_entry.get())  # Convert to float
    manual = manual_entry.get()
    maps = maps_entry.get()

    dataframe = read_excel_file("game_collection.xlsx")
    if dataframe is not None:
        dataframe.loc[selected_item_index, "Title"] = title
        dataframe.loc[selected_item_index, "System"] = system
        dataframe.loc[selected_item_index, "Genre"] = genre
        dataframe.loc[selected_item_index, "Price Charting"] = price_charting
        dataframe.loc[selected_item_index, "Manual"] = manual
        dataframe.loc[selected_item_index, "Maps"] = maps

        write_excel_file(dataframe, "game_collection.xlsx")
        update_display(dataframe)
        clear_fields()

def populate_fields(event):
    global selected_item_index
    selected_item_index = display_tree.index(display_tree.selection()[0])
    selected_item = display_tree.item(display_tree.selection())["values"]
    if selected_item:
        title_entry.delete(0, tk.END)
        title_entry.insert(0, selected_item[0])
        system_entry.delete(0, tk.END)
        system_entry.insert(0, selected_item[1])
        genre_entry.delete(0, tk.END)
        genre_entry.insert(0, selected_item[2])
        price_charting_entry.delete(0, tk.END)
        price_charting_entry.insert(0, selected_item[3])
        manual_entry.delete(0, tk.END)
        manual_entry.insert(0, selected_item[4])
        maps_entry.delete(0, tk.END)
        maps_entry.insert(0, selected_item[5])

def delete_entry():
    global selected_item_index
    dataframe = read_excel_file("game_collection.xlsx")
    if dataframe is not None and selected_item_index is not None:
        dataframe.drop(index=selected_item_index, inplace=True)
        write_excel_file(dataframe, "game_collection.xlsx")
        update_display(dataframe)
        clear_fields()
        selected_item_index = None
# Function to read the excel file and return the data as a dataframe
def read_excel_file(filename):
    try:
        data = pd.read_excel(filename)
        return data
    except Exception as e:
        print(f"Error reading excel file: {e}")
        return None


# Function to write the dataframe to an excel file
def write_excel_file(data, filename):
    try:
        data.to_excel(filename, index=False)
        print(f"Data written to {filename} successfully")
    except Exception as e:
        print(f"Error writing excel file: {e}")


# Function to add a new entry to the collection
def add_entry():
    title = title_entry.get()
    system = system_entry.get()
    genre = genre_entry.get()
    price_charting = price_charting_entry.get()
    manual = manual_entry.get()
    maps = maps_entry.get()

    if not title:
        print("Title cannot be empty")
        return

    new_entry = {
        "Title": title, "System": system, "Genre": genre,
        "Price Charting": price_charting, "Manual": manual, "Maps": maps
    }
    dataframe = read_excel_file("game_collection.xlsx")
    if dataframe is None:
        dataframe = pd.DataFrame(columns=["Title", "System", "Genre",
                                          "Price Charting", "Manual", "Maps"])
    dataframe = pd.concat([dataframe, pd.DataFrame([new_entry])], ignore_index=True)
    write_excel_file(dataframe, "game_collection.xlsx")

    # Update the display with the new data
    #update_display(dataframe)
    sort_collection("Title")


# Function to clear the input fields
def clear_fields():
    title_entry.delete(0, tk.END)
    system_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    price_charting_entry.delete(0, tk.END)
    manual_entry.delete(0, tk.END)
    maps_entry.delete(0, tk.END)


# Function to sort the collection by a specific header
def sort_collection(header):
    dataframe = read_excel_file("game_collection.xlsx")
    if dataframe is not None:
        sorted_dataframe = dataframe.sort_values(by=header)
        write_excel_file(sorted_dataframe, "game_collection.xlsx")
        update_display(sorted_dataframe)


# Function to update the display with new data
def update_display(dataframe):
    # Update the number of games label
    num_games_value_label.config(text=str(len(dataframe)))

    # Update the total value label
    total_value = dataframe["Price Charting"].sum()
    total_value_value_label.config(text="${:.2f}".format(total_value))

    display_tree.delete(*display_tree.get_children())  # Clear the current content
    for index, row in dataframe.iterrows():
        display_tree.insert("", "end", values=(
            row["Title"], row["System"], row["Genre"], row["Price Charting"], row["Manual"], row["Maps"]
        ))


# Create the main window
window = tk.Tk()
window.title("Game Collection Entry")

# Create the input fields and labels
title_label = tk.Label(window, text="Title:")
title_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
title_entry = tk.Entry(window)
title_entry.grid(row=0, column=1)

system_label = tk.Label(window, text="System:")
system_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
system_entry = tk.Entry(window)
system_entry.grid(row=1, column=1)

genre_label = tk.Label(window, text="Genre:")
genre_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
genre_entry = tk.Entry(window)
genre_entry.grid(row=2, column=1)

price_charting_label = tk.Label(window, text="Price Charting:")
price_charting_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
price_charting_entry = tk.Entry(window)
price_charting_entry.grid(row=3, column=1)

manual_label = tk.Label(window, text="Manual:")
manual_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
manual_entry = tk.Entry(window)
manual_entry.grid(row=4, column=1)

maps_label = tk.Label(window, text="Maps:")
maps_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")
maps_entry = tk.Entry(window)
maps_entry.grid(row=5, column=1)

# Create the submit button
submit_button = tk.Button(window, text="Submit", command=add_entry)
submit_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)


# Create the update button for editing existing entries
update_button = tk.Button(window, text="Update", command=update_entry)
update_button.grid(row=6, column=1, padx=10, pady=10)

# Create the clear button
clear_button = tk.Button(window, text="Clear", command=clear_fields)
clear_button.grid(row=6, column=3, padx=10, pady=10)
#Create Delete Button

delete_button = tk.Button(window, text="Delete", command=delete_entry)
delete_button.grid(row=6, column=2, padx=10, pady=10)

from tkinter import ttk
window = tk.Tk()
window.title("Game Collection")

# ...

# Create the display Treeview widget
display_tree = ttk.Treeview(window, columns=("Title", "System", "Genre", "Price Charting", "Manual", "Maps"),
                            displaycolumns=(0, 1, 2, 3, 4, 5), height=10)
display_tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
vertical_scrollbar = ttk.Scrollbar(window, orient="vertical", command=display_tree.yview)
display_tree.configure(yscrollcommand=vertical_scrollbar.set)
vertical_scrollbar.grid(row=7, column=2, sticky="ns")



# Add column headings
display_tree.heading("#1", text="Title")
display_tree.heading("#2", text="System")
display_tree.heading("#3", text="Genre")
display_tree.heading("#4", text="Price Charting")
display_tree.heading("#5", text="Manual")
display_tree.heading("#6", text="Maps")

# Bind double-click event to populate_fields function
display_tree.bind("<Double-1>", populate_fields)

# Create the sort buttons
sort_title_button = tk.Button(window, text="Sort by Title", command=lambda: sort_collection("Title"))
sort_title_button.grid(row=8, column=0, padx=10, pady=5, sticky="w")

# Display the number of games
num_games_label = tk.Label(window, text="Number of Games:")
num_games_label.grid(row=8, column=0, padx=10, pady=5, sticky="e")
num_games_value_label = tk.Label(window, text="0")
num_games_value_label.grid(row=8, column=1, padx=10, pady=5, sticky="w")

# Display the total value
total_value_label = tk.Label(window, text="Total Value:")
total_value_label.grid(row=9, column=0, padx=10, pady=5, sticky="e")
total_value_value_label = tk.Label(window, text="0.00")
total_value_value_label.grid(row=9, column=1, padx=10, pady=5, sticky="w")

exit_system_button = tk.Button(window, text="Exit", command=lambda: exit())
exit_system_button.grid(row=10, column=2, padx=10, pady=5, sticky="e")

update_drive_button = tk.Button(window, text="Save to GDrive", command=lambda: gdrive_upload.main()) # "game_collection.xlsx"))
update_drive_button.grid(row=11, column=0, padx=10, pady=5, sticky="e")

update_drive_button = tk.Button(window, text="Update From GDrive", command=lambda: gdrive_sync.gdrive_sync())#gdrive_upload.check_date()) # "game_collection.xlsx"))
update_drive_button.grid(row=12, column=0, padx=10, pady=5, sticky="e")


sort_system_button = tk.Button(window, text="Sort by System", command=lambda: sort_collection("System"))
sort_system_button.grid(row=8, column=1, padx=10, pady=5, sticky="e")

sort_genre_button = tk.Button(window, text="Sort by Genre", command=lambda: sort_collection("Genre"))
sort_genre_button.grid(row=9, column=0, padx=10, pady=5, sticky="w")

sort_price_button = tk.Button(window, text="Sort by Price Charting", command=lambda: sort_collection("Price Charting"))
sort_price_button.grid(row=9, column=1, padx=10, pady=5, sticky="e")

sort_manual_button = tk.Button(window, text="Sort by Manual", command=lambda: sort_collection("Manual"))
sort_manual_button.grid(row=10, column=0, padx=10, pady=5, sticky="w")

sort_maps_button = tk.Button(window, text="Sort by Maps", command=lambda: sort_collection("Maps"))
sort_maps_button.grid(row=10, column=1, padx=10, pady=5, sticky="e")


# Read and display the initial collection
if not os.path.exists("game_collection.xlsx"):
    initial_df = pd.DataFrame(columns=["Title", "System", "Genre",
                                       "Price Charting", "Manual", "Maps"])
    write_excel_file(initial_df, "game_collection.xlsx")

dataframe = read_excel_file("game_collection.xlsx")
if dataframe is not None:
    update_display(dataframe)  # Update the Treeview with initial data
else:
    display_tree.insert("", "end", values=("No data found", "", "", "", "", ""))

# Start the main event loop
window.mainloop()
