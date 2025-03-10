import random
import string
import tkinter as tk
import json
import os
from tkinter import ttk
from tkinter import messagebox

def generate_password(length, include_uppercase, include_numbers, include_symbols):
    characters = string.ascii_lowercase
    if include_uppercase: # Check to see if password will contain any uppercase characters
        characters += string.ascii_uppercase
    if include_numbers: # Check to see if password will contain any numbers
        characters += string.digits

    # My preferred default counts
    num_uppercase = 1 if include_uppercase else 0  # 1 uppercase if selected
    num_numbers = 3 if include_numbers else 0    # 3 numbers if option is selected
    num_symbols = 2 if include_symbols else 0    # 2 special characters if option is selected
    num_lowercase = length - num_uppercase - num_numbers - num_symbols

    if num_lowercase < 0: 
        num_lowercase = 0
        if num_symbols + num_numbers + num_uppercase > length:
            num_symbols = max(0, length - num_uppercase - num_numbers) 
        if num_numbers + num_uppercase > length:
            num_numbers = max(0, length - num_uppercase)
   
    password_list = []
    password_list.extend(random.choice(string.ascii_uppercase) for _ in range(num_uppercase))
    password_list.extend(random.choice(string.digits) for _ in range(num_numbers))
    password_list.extend(random.choice(string.punctuation) for _ in range(num_symbols))
    password_list.extend(random.choice(string.ascii_lowercase) for _ in range(num_lowercase))

    password = "".join(password_list)

    # Reshuffles the password after password is created
    password_list = list(password)
    random.shuffle(password_list)
    password = "".join(password_list)

    return password

# Function to check the strength of the newly created password
def check_strength(password):
    strength = 0
    if len(password) >= 15:
        strength += 1
    if any(c.islower() for c in password):
        strength += 1
    if any(c.isupper() for c in password):
        strength += 1
    if any(c.isdigit() for c in password):
        strength += 1
    if any(c in string.punctuation for c in password):
        strength += 1

    # Output of password strength that the user sees after creating password
    if strength <= 2:
        return "Weak"
    elif strength <= 4:
        return "Medium"
    else:
        return "Strong"

def generate_and_display():
    try:
        length = int(length_entry.get())
        if length <= 0:
            result_label.config(text="Invalid length: Must be greater than 0")
            return
    except ValueError:
        result_label.config(text="Invalid length: Please enter a number.")
        return

    uppercase = uppercase_var.get()
    numbers = numbers_var.get()
    symbols = symbols_var.get()

    password = generate_password(length, uppercase, numbers, symbols)
    strength = check_strength(password)
    result_label.config(text=f"Generated Password: {password}\nStrength: {strength}")
    generated_password.set(password)  # Store the password


# Function to save the password using JSON storage
def save_password():
    username = username_entry.get() # allows user to save a username for the newly created password
    website = website_entry.get() # allows user to enter the website for the username and newly created password
    password = generated_password.get()  # Retrieves the newly generated password

    if not username or not website or not password:
        messagebox.showerror("Error", "Please fill in all fields (username, website, and generate a password).") # Error catch if the user presses the save password button before entering any information or getting a new password
        return

    data = {} # Dictionary 
    filepath = "passwords.json" # file path to json storage

    # Check to ensure that the file exists and loads the existing data
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error reading passwords.json.  File may be corrupt.")
            return  # Exit if we can't read the file

    # Check the file for duplicates
    if website in data and username in data[website]:
        if not messagebox.askyesno("Duplicate Entry", "A password for this website and username already exists. Would you like to overwrite?"):
            return

    # Structure the data within the JSON to avoid username/website collisions.
    if website not in data:
        data[website] = {}  # Create a dictionary for the website
    data[website][username] = password  # Store password under website -> username

    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)  # Use indent for readability
        messagebox.showinfo("Success", "Password saved successfully!")
        # Clear fields after saving
        username_entry.delete(0, tk.END)
        website_entry.delete(0, tk.END)
        generated_password.set("") # clear saved password
        result_label.config(text="")


    except Exception as e:
        messagebox.showerror("Error", f"Failed to save password: {e}")


# Graphic User Interface
window = tk.Tk()
window.title("Password Generator")
window.geometry("500x450") # size of the window
style = ttk.Style()
style.theme_use('default')  # Themed used 
main_frame = ttk.Frame(window, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)


# Desired Length of password
length_label = ttk.Label(main_frame, text="Desired Password Length:")
length_label.grid(row=0, column=0, sticky=tk.W, pady=5)  # Use grid layout, sticky=tk.W
length_entry = ttk.Entry(main_frame, width=5)
length_entry.grid(row=0, column=1, sticky=tk.W, pady=5)

# Checkbox if user wants uppercase
uppercase_var = tk.BooleanVar(value=True)  
uppercase_check = ttk.Checkbutton(main_frame, text="Include Uppercase", variable=uppercase_var)
uppercase_check.grid(row=1, column=0, sticky=tk.W, pady=5)

# Checkbox if user wants numbers
numbers_var = tk.BooleanVar(value=True)
numbers_check = ttk.Checkbutton(main_frame, text="Include Numbers", variable=numbers_var)
numbers_check.grid(row=2, column=0, sticky=tk.W, pady=5)

# Checkbox if user wants special characters
symbols_var = tk.BooleanVar(value=True)
symbols_check = ttk.Checkbutton(main_frame, text="Include Symbols", variable=symbols_var)
symbols_check.grid(row=3, column=0, sticky=tk.W, pady=5)

# Button to generate password
generate_button = ttk.Button(main_frame, text="Generate Password", command=generate_and_display)
generate_button.grid(row=4, column=0, columnspan=2, pady=10)

# Result Label
result_label = ttk.Label(main_frame, text="", wraplength=450)  
result_label.grid(row=5, column=0, columnspan=2, pady=5)

# --- Password Saving Section ---
save_frame = ttk.LabelFrame(main_frame, text="Save Password", padding=10) 
save_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")

# Box to enter the username
username_label = ttk.Label(save_frame, text="Username:")
username_label.grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
username_entry = ttk.Entry(save_frame)
username_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

# Box to enter the website
website_label = ttk.Label(save_frame, text="Website:")
website_label.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
website_entry = ttk.Entry(save_frame)
website_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

# Button to save password
save_button = ttk.Button(save_frame, text="Save Password", command=save_password)
save_button.grid(row=2, column=0, columnspan=2, pady=10)

# String variable to hold generated password
generated_password = tk.StringVar()


window.mainloop()