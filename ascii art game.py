import tkinter as tk
from tkinter import colorchooser
import random
import time
import json

# Store ASCII art pictures with their rarities
pictures = [
    {"art": """
       (\_/)
      (='.'=)
      (")_(")
    """, "rarity": "common"},
    {"art": """
     _,-._
    / \_/ \
    >-(_)-<
    \_/ \_/
      `-'
    """, "rarity": "common"},
    {"art": """
      /\_/\
     ( o.o )
      > ^ <
    """, "rarity": "common"},
    {"art": """
        .--""--.
     .'          `.
    |   O      O   |
     \  .--""--.  /
      '._______.'
        ||| |||
        ||| |||
    """, "rarity": "uncommon"},
    {"art": """
      _.--""--._
    .'          `.
    |   ^    ^   |
     \  .--""--.  /
      '._______.'
    """, "rarity": "uncommon"},
    {"art": """
      ( o o )
     /------\/
      |    ||
       \  /\
       `-'
    """, "rarity": "unusual"},
    # ... (Add more pictures with different rarities)
]

# Rarity probabilities
rarities = {
    "common": 50000,
    "uncommon": 20000,
    "unusual": 10000,
    "remarkable": 5000,
    "rare": 3333,
    "outstanding": 2500,
    "exceptional": 2000,
    "strange": 1666,
    "master": 1428,
    "elite": 1250,
    "arcane": 1111,
    "unique": 1000,
    "epic": 200,
    "eldritch": 100,
    "legendary": 20,
    "divine": 10,
    "mythic": 2,
    "super mythic": 1,
    "ultra mythic": 0.6666  # Approximated
}

def get_random_picture():
    global rarities

    if not pictures:  # Check if the pictures list is empty
        return None

    try:
        # Use random.choices with weights based on rarity probabilities
        picture = random.choices(pictures, weights=[rarities[p["rarity"]] for p in pictures])[0]
    except KeyError:
        # Handle the case where a rarity name is not found in the rarities dictionary
        print("Error: Invalid rarity name found in pictures list.")
        return None

    # Add "cracked" effect for rarities below exceptional
    if rarities[picture["rarity"]] > 2000:
        # Implement your "cracking" effect here
        # For example, you could replace some characters with " " or "_"
        pass

    return picture

def show_picture():
    global elapsed_time, last_picture_time, keep_art
    elapsed_time += 1
    timer_label.config(text=f"Time played: {elapsed_time // 60} minutes {elapsed_time % 60} seconds")
    if time.time() - last_picture_time >= 60:
        new_picture = get_random_picture()
        if new_picture:
            picture_text.delete("1.0", tk.END)  # Clear previous content
            picture_text.insert(tk.END, new_picture["art"])  # Insert new picture
            if keep_art:
                try:
                    current_rarity = rarities[rarity_label.cget("text").split(": ")[-1]]
                except KeyError:
                    current_rarity = rarities["common"]
                new_rarity = rarities[new_picture["rarity"]]
                if new_rarity <= current_rarity:
                    rarity_label.config(text=f"Rarity: {new_picture['rarity']}")
            else:
                rarity_label.config(text=f"Rarity: {new_picture['rarity']}")
        else:
            picture_text.delete("1.0", tk.END)
            picture_text.insert(tk.END, "No picture found.")
            rarity_label.config(text="")
        last_picture_time = time.time()
    root.after(1000, show_picture)

def save_game():
    data = {
        "elapsed_time": elapsed_time,
        "bg_color": bg_color,
        "keep_art": keep_art
    }
    with open("game_save.json", "w") as f:
        json.dump(data, f)

def load_game():
    global elapsed_time, bg_color, keep_art
    try:
        with open("game_save.json", "r") as f:
            data = json.load(f)
            elapsed_time = data.get("elapsed_time", 0)
            bg_color = data.get("bg_color", "white")
            keep_art = data.get("keep_art", False)
    except FileNotFoundError:
        pass

def open_settings():
    global bg_color, keep_art

    def change_bg_color():
        global bg_color
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code[1]:
            bg_color = color_code[1]
            settings_window.config(bg=bg_color)
            root.config(bg=bg_color)

    def toggle_keep_art():
        global keep_art
        keep_art = keep_art_var.get()

    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("500x500")
    settings_window.resizable(False, False)
    settings_window.config(bg=bg_color)

    bg_color_button = tk.Button(settings_window, text="Change Background Color", command=change_bg_color)
    bg_color_button.pack(pady=20)

    keep_art_var = tk.BooleanVar(value=keep_art)
    keep_art_checkbox = tk.Checkbutton(settings_window, text="Keep Existing Art", variable=keep_art_var, command=toggle_keep_art)
    keep_art_checkbox.pack()

def close_game():
    save_game()
    root.destroy()

def open_minigames():
    pass

# Initialize Tkinter
root = tk.Tk()
root.title("ASCII Art Collector")
root.geometry("300x500")
root.resizable(False, False)

bg_color = "white"
keep_art = False
root.config(bg=bg_color)

# Load saved game data
elapsed_time = 0
last_picture_time = time.time()
load_game()

# Picture display
picture_text = tk.Text(root, font=("Courier New", 16), width=30, height=10)  # Use Text widget
picture_text.pack(pady=20)
rarity_label = tk.Label(root, text="", bg=bg_color)
rarity_label.pack()

# Timer
timer_label = tk.Label(root, text=f"Time played: {elapsed_time // 60} minutes {elapsed_time % 60} seconds", bg=bg_color)
timer_label.pack(pady=20)

# Create a frame to hold the buttons
button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(side="bottom", fill="x")

# Buttons
settings_button = tk.Button(button_frame, text="Settings", command=open_settings)
settings_button.pack(side="left", padx=5, pady=5)

close_button = tk.Button(button_frame, text="Close", command=close_game)
close_button.pack(side="left", padx=5, pady=5)

minigames_button = tk.Button(button_frame, text="Minigames", command=open_minigames)
minigames_button.pack(side="left", padx=5, pady=5)

# Start the game loop
show_picture()

# Save game on exit
root.protocol("WM_DELETE_WINDOW", save_game)

root.mainloop()
