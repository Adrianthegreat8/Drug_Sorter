"""
GUI_version4_reset_drugs_and_assistants.py
runs the gui and calls the backend
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import backend_version_2 as be
import os
import json


class PatientApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.create_window()

        # Read from config.json and set instance variables
        self.config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.json')
        with open(self.config_path, 'r') as config_file:
            config_data = json.load(config_file)
        self.file_name = config_data.get('file_name')
        self.saved_directory = config_data.get('save_directory')

        self.rows = 0
        self.static_stringvars = []  # for storing fixed data like name, identifier
        self.drugs_used = []
        self.assistants = []
        self.create_widgets()
        # self.bind('<Return>', self.handle_return_key)

        self.patient_information = {
            'date': '',
            'patient_name': {'First_Name': '', 'Last_Name': ''},
            'patient_name_one_word': '',
            'patient_identifier': '',
            'drugs_used': {},
            'doctor': '',
            'assistant(s)': []
        }

    def create_window(self):
        # Set the title
        self.title('Patient information system')

        # Set the window size
        window_width, window_height = 600, 400

        # Get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Find the center position
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # Set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    def create_widgets(self):
        self.config_menu()

        # Frame for static fields
        self.static_frame = ttk.Frame(self)
        self.static_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        self.static_frame.columnconfigure(1, weight=1)

        # Frame for dynamic fields
        self.dynamic_frame = ttk.Frame(self)
        self.dynamic_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.dynamic_frame.columnconfigure(1, weight=1)

        # Frame for buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=2, column=0, padx=10, pady=5)

        self.grid_columnconfigure(0, weight=1)  # Ensures the main window expands content

        # Initialize static fields
        self.init_static_fields()

        # Initialize buttons
        self.init_buttons()

    def config_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Set Save Directory", command=self.set_saved_directory)
        file_menu.add_command(label="Submit", command=self.submit_button_command)

    def set_saved_directory(self):
        # Open a dialog to select a directory
        directory = filedialog.askdirectory()
        if directory:
            self.saved_directory = directory
            self.update_config_attribute('save_directory',directory)
            messagebox.showinfo("Directory Set", f"Files will be saved in: {self.saved_directory}")
            # write to config.json new default directory

    def load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found at {self.config_path}")
        with open(self.config_path, 'r') as config_file:
            return json.load(config_file)

    def save_config(self, config_data):
        with open(self.config_path, 'w') as config_file:
            json.dump(config_data, config_file, indent=2)

    def update_config_attribute(self, key, value):
        # Load the existing configuration
        config = self.load_config()

        # Update the desired attribute
        config[key] = value

        # Save the updated configuration back to config.json
        self.save_config(config)
        print(f"Updated {key} to {value}")

    def init_static_fields(self):
        self.first_name_var = tk.StringVar()
        self.first_name_entry = self.create_entry_field("First Name:", 0, self.first_name_var, self.static_frame)

        self.last_name_var = tk.StringVar()
        self.last_name_entry = self.create_entry_field("Last Name:", 1, self.last_name_var, self.static_frame)

        self.identifier_var = tk.StringVar()
        self.identifier_entry = self.create_entry_field("Identifier:", 2, self.identifier_var, self.static_frame)

        self.date_var = tk.StringVar()
        self.date_entry = self.create_entry_field('Date:', 3, self.date_var, self.static_frame)

        self.doctor_var = tk.StringVar()
        self.doctor_entry = self.create_entry_field('Doctor:', 4, self.doctor_var, self.static_frame)

    def create_entry_field(self, label_text, row, variable, frame):
        ttk.Label(frame, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        self.rows += 1
        entry = ttk.Entry(frame, textvariable=variable)
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        self.static_stringvars.append(variable)
        return entry, variable  # Return both the entry widget and its associated StringVar

    def init_buttons(self):
        self.add_drug_button = ttk.Button(self.button_frame, text="Add Drug", command=self.add_drug_field)
        self.add_drug_button.grid(row=0, column=0, pady=10, padx=10, sticky='ew')

        self.add_assistant_button = ttk.Button(self.button_frame, text="Add Assistant",
                                               command=self.add_assistant_field)
        self.add_assistant_button.grid(row=0, column=1, pady=10, padx=10, sticky='ew')

        self.submit_button = ttk.Button(self.button_frame, text="Submit", command=self.submit_button_command)
        self.submit_button.grid(row=0, column=2, pady=10, padx=10, sticky="ew")

    def add_drug_field(self):
        # Increment the row for new fields
        current_row = self.rows
        self.rows += 2  # Prepare for the next widget (we're adding two fields per drug)

        # Create variables to store drug name and dosage input
        drug_var = tk.StringVar()
        dosage_var = tk.StringVar()
        wasted_var = tk.StringVar()

        # Create and place the drug name label and entry field
        ttk.Label(self.dynamic_frame, text=f"Drug #{len(self.drugs_used) + 1}:").grid(row=current_row, column=0,
                                                                                      padx=10, pady=5, sticky="we")
        drug_entry = ttk.Entry(self.dynamic_frame, textvariable=drug_var)
        drug_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")

        # Create and place the dosage label and entry field
        ttk.Label(self.dynamic_frame, text="Dosage:").grid(row=current_row + 1, column=0, padx=10, pady=5, sticky="we")
        dosage_entry = ttk.Entry(self.dynamic_frame, textvariable=dosage_var)
        dosage_entry.grid(row=current_row + 1, column=1, padx=10, pady=5, sticky="ew")

        # Create and place the wasted label and entry field
        ttk.Label(self.dynamic_frame, text="Wasted:").grid(row=current_row + 2, column=0, padx=10, pady=5, sticky="we")
        wasted_entry = ttk.Entry(self.dynamic_frame, textvariable=wasted_var)
        wasted_entry.grid(row=current_row + 2, column=1, padx=10, pady=5, sticky="ew")

        # Store the drug name and dosage entries for later use (if needed)
        self.drugs_used.append((drug_var, dosage_var, wasted_var))
        self.rows += 1  # Increment rows to make space for the "Add Drug" button

    def add_assistant_field(self):
        # Increment the row for new fields
        current_row = self.rows
        self.rows += 1  # Prepare for the next widget (we're adding two fields per drug)

        # Create variables to store drug name and dosage input
        assistant = tk.StringVar()

        # Create and place the drug name label and entry field
        ttk.Label(self.dynamic_frame, text=f"Assistant #{len(self.assistants) + 1}:").grid(row=current_row, column=0,
                                                                                           padx=10,
                                                                                           pady=5, sticky="we")
        assistant_entry = ttk.Entry(self.dynamic_frame, textvariable=assistant)
        assistant_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")

        # Store the assistant name  for later use (if needed)
        self.assistants.append(assistant)

    def submit_button_command(self):
        if not self.saved_directory:  # This is placed here so that fields are not cleared if a dir is not set
            messagebox.showerror("Error", "Please set a save directory first.")
            return
        self.submit_patient_info()
        self.clear_fields()
        self.reset_fields()

    def reset_fields(self):
        self.reset_drug_field()
        self.reset_assistant_field()
        self.reset_dynamic_frame()
        self.update_idletasks()

    def reset_drug_field(self):
        self.rows = 0
        self.drugs_used.clear()

    def reset_assistant_field(self):
        self.rows = 0
        self.assistants.clear()

    def clear_fields(self):
        # clear static fields
        for i in self.static_stringvars:
            i.set('')

        for i in self.assistants:
            i.set('')

        for i in self.drugs_used:
            for j in i:
                j.set('')

    def reset_dynamic_frame(self):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()
        self.dynamic_frame.destroy()
        self.dynamic_frame = ttk.Frame(self)
        self.dynamic_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.dynamic_frame.columnconfigure(1, weight=1)

    def submit_patient_info(self):
        static_variable_list = [i.get() for i in self.static_stringvars]
        assistants_list = [i.get() for i in self.assistants]
        drugs_used_dict = {drug.get(): [dosage.get(), wasted.get()] for drug, dosage, wasted in self.drugs_used}

        self.patient_information = {
            'date': static_variable_list[3],
            'patient_name': {'First_Name': static_variable_list[0], 'Last_Name': static_variable_list[1]},
            'patient_name_one_word': '',
            'patient_identifier': static_variable_list[2],
            'drugs_used': drugs_used_dict,
            'doctor': static_variable_list[4],
            'assistant(s)': assistants_list
        }

        full_file_path = os.path.join(self.saved_directory, self.file_name + '.xlsx')
        # debugging
        # print('saved dir:', self.saved_directory)
        # print('file name:', self.file_name)
        # print('Saving to:', full_file_path)
        # print(type(full_file_path))
        be.save_patient_data(self.patient_information, full_file_path)


def main():
    app = PatientApp()
    app.mainloop()


if __name__ == '__main__':
    main()
