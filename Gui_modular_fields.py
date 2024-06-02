import tkinter as tk
from tkinter import ttk, messagebox


class PatientApp(tk.Tk):
    def __init__ (self):
        super().__init__()
        self.creat_window()
        self.rows = 0
        self.fields = [] # for storing fixed data like name, identifier
        self.drugs_used = []
        self.assistants = []
        self.create_widgets()
        self.bind('<Return>', self.handle_return_key)

        self.patient_information = {
        'date': '',
        'patient_name': {'First_Name': '', 'Last_Name': ''},
        'patient_name_one_word': '',
        'patient_identifier': '',
        'drugs_used': {},
        'doctor': '',
        'assistant(s)': []
    }

        self.enter_patient_info()

    def creat_window (self):
        # Set the title
        self.title('Patient information system')
        
        # Set the window size
        window_width, window_height = 600,400
        
        # Get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Find the center position
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        
        # Set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    def create_entry_field(self, label_text, row, variable):
        ttk.Label(self.input_frame, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky="w")
        self.rows += 1
        entry = ttk.Entry(self.input_frame, textvariable=variable)
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        return entry, variable  # Return both the entry widget and its associated StringVar

    def add_drug_field(self):
        # Increment the row for new fields
        current_row = self.rows
        self.rows += 2  # Prepare for the next widget (we're adding two fields per drug)

        # Create variables to store drug name and dosage input
        drug_var = tk.StringVar()
        dosage_var = tk.StringVar()

        # Create and place the drug name label and entry field
        ttk.Label(self.input_frame, text=f"Drug #{len(self.drugs_used) + 1}:").grid(row=current_row, column=0, padx=10,
                                                                                    pady=5, sticky="w")
        drug_entry = ttk.Entry(self.input_frame, textvariable=drug_var)
        drug_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")

        # Create and place the dosage label and entry field
        ttk.Label(self.input_frame, text="Dosage:").grid(row=current_row + 1, column=0, padx=10, pady=5, sticky="w")
        dosage_entry = ttk.Entry(self.input_frame, textvariable=dosage_var)
        dosage_entry.grid(row=current_row + 1, column=1, padx=10, pady=5, sticky="ew")

        # Store the drug name and dosage entries for later use (if needed)
        self.drugs_used.append((drug_var, dosage_var))

        # Reposition the "Add Drug" button to be below the latest drug fields
        self.add_drug_button.grid_forget()  # Remove the button from its current position
        self.add_drug_button.grid(row=self.rows, column=1, pady=10, padx=10, sticky='ew')
        self.rows += 1  # Increment rows to make space for the "Add Drug" button

        # Reposition the "Submit" button to be below the "Add Drug" button
        self.submit_button.grid_forget()  # Remove the button from its current position
        self.submit_button.grid(row=self.rows, column=1, pady=10, padx=10, sticky="ew")
        self.rows += 1  # Update rows for future additions

    def add_assistant_field(self):
        # Increment the row for new fields
        current_row = self.rows
        self.rows += 1  # Prepare for the next widget (we're adding one fields per assistnat)

        # Create variables to store drug name and dosage input
        assistant = tk.StringVar()

        # Create and place the drug name label and entry field
        ttk.Label(self.input_frame, text=f"Assistant #{len(self.assistants) + 1}:").grid(row=current_row, column=0, padx=10,
                                                                                    pady=5, sticky="w")
        assistant_entry = ttk.Entry(self.input_frame, textvariable=assistant)
        assistant_entry.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")

        # Store the drug name and dosage entries for later use (if needed)
        self.assistants.append(assistant)

        # Reposition the "Add Drug" button to be below the latest drug fields
        self.add_drug_button.grid_forget()  # Remove the button from its current position
        self.add_drug_button.grid(row=self.rows, column=1, pady=10, padx=10, sticky='ew')
        self.rows += 1  # Increment rows to make space for the "Add Drug" button

        # Reposition the "Submit" button to be below the "Add Drug" button
        self.submit_button.grid_forget()  # Remove the button from its current position
        self.submit_button.grid(row=self.rows, column=1, pady=10, padx=10, sticky="ew")
        self.rows += 1  # Update rows for future additions


    def create_widgets(self):
        # Create a frame for input fields
        self.input_frame = ttk.Frame(self)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Configure the grid to expand the frame column
        self.input_frame.columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Make the frame expand with the window
        
        ### Fields ###

            ## Field Variables ##

        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.identifier_var = tk.StringVar()

        # Example of adding more field variables
        
        # self.additional_var_1 = tk.StringVar()

            ## Initialize Fields ##
        
        self.first_name_entry = self.create_entry_field("First Name:", 0, self.first_name_var)
        self.last_name_entry = self.create_entry_field("Last Name:", 1, self.last_name_var)
        self.identifier_entry = self.create_entry_field("Identifier:", 2, self.identifier_var)

        # Example of adding more fields
        
        # self.additional_entry_1 = self.create_entry_field("Additional Field 1:", 3, self.additional_var_1)

        self.add_drug_button = ttk.Button(self.input_frame, text="Add Drug", command=self.add_drug_field)
        self.add_drug_button.grid(row=self.rows, column=1, pady=10, padx=10, sticky='ew')
        self.rows += 1  # Increment row for the next widget

        # add assistants here

        self.add_assistant_button = ttk.Button(self.input_frame, text="Add Assistant", command=self.add_assistant_field)
        self.add_assistant_button.grid(row=self.rows, column=1, pady=10, padx=10, sticky='ew')
        self.rows += 1  # Increment row for the next widget


        self.submit_button = ttk.Button(self.input_frame, text="Submit", command=self.enter_patient_info)
        self.submit_button.grid(row=self.rows, column=1, pady=10, padx=10, sticky="ew")
        self.rows += 1  # Increment row for the next widget

        ### End Fields ###


        # Set initial focus
        self.first_name_entry[0].focus_set()

    def handle_return_key (self, event): #This will scroll through the widgets using <Return> for ease of use
        
        current_field = self.focus_get()

        if current_field in self.fields:
            current_index = self.fields.index(current_field)
            next_index = (current_index + 1) % len(self.fields) #Wraps around to the first field after 5
            self.fields[next_index].focus_set()
    

    def enter_patient_info(self):
        # Retrieve data from the input fields
        first_name = self.first_name_var.get()

        last_name = self.last_name_var.get()

        identifier = self.identifier_var.get()


        # Here, you would usually validate the input and create a Patient object
        # For demonstration, we'll just print the inputs
        print(first_name, last_name, identifier)

        drugs_used_dict = {}

        for drug_var, dosage_var in self.drugs_used:
            drug_name = drug_var.get()
            dosage = dosage_var.get()
            drugs_used_dict[drug_name] = dosage  # Store drug name as key and dosage as value in the dict

        assistants_list = []

        for assistant_var in self.assistants:
            assistant_name = assistant_var.get
            assistants_list.append(assistant_name)

            # Construct the patient_information dict with the correct drugs_used data
        self.patient_information = {
            'date': '',
            'patient_name': {'First_Name': first_name, 'Last_Name': last_name},
            'patient_name_one_word': first_name + " " + last_name,
            'patient_identifier': identifier,
            'drugs_used': drugs_used_dict,
            'doctor': '',
            'assistant(s)': assistants_list
        }

        print(self.patient_information)

        self.clear_fields()

    def clear_fields(self):
        """Clears all input fields in the form."""
        # Clear fixed fields
        for var in [self.first_name_var, self.last_name_var, self.identifier_var]:
            var.set("")

        # Clear dynamic fields (e.g., drugs)

        for i in self.drugs_used:
            for j in i:
                j.set('')

if __name__ == "__main__":
    app = PatientApp()
    app.mainloop()
