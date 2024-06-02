import tkinter as tk
from tkinter import ttk

class PatientApp(tk.Tk):
    def __init__ (self):
        super().__init__()
        self.creat_window()
        self.fields = []
        self.create_widgets()
        self.bind('<Return>', self.handle_return_key)

    def creat_window (self):
        # Set the title
        self.title('Patient information system')
        
        # Set the window size
        window_width = 400
        window_height = 200
        
        # Get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Find the center position
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        
        # Set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    def create_widgets(self):
        # Create a frame for input fields
        self.input_frame = ttk.Frame(self)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Configure the grid to expand the frame column
        self.input_frame.columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Make the frame expand with the window
        
        ###Fields###

        # Patient's First Name
        ttk.Label(self.input_frame, text="First Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.first_name_var = tk.StringVar()
        first_name_entry = ttk.Entry(self.input_frame, textvariable=self.first_name_var)
        first_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.fields.append(first_name_entry)

        # Patient's Last Name
        ttk.Label(self.input_frame, text="Last Name:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.last_name_var = tk.StringVar()
        last_name_entry = ttk.Entry(self.input_frame, textvariable=self.last_name_var)
        last_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.fields.append(last_name_entry)

        # Patient Identifier
        ttk.Label(self.input_frame, text="Identifier:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.identifier_var = tk.StringVar()
        patient_identifier = ttk.Entry(self.input_frame, textvariable=self.identifier_var)
        patient_identifier.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.fields.append(patient_identifier)
        
        ###End Fields###

        # Submit info button
        self.submit_button = ttk.Button(self.input_frame, text="Submit", command=self.submit_patient_info)
        self.submit_button.grid(row=3, column=1, columnspan=1, pady=10, padx=10, sticky="ew")

        # Set initial focus
        first_name_entry.focus_set()

    def submit_patient_info(self):
        # Retrieve data from the input fields
        first_name = self.first_name_var.get()
        last_name = self.last_name_var.get()
        identifier = self.identifier_var.get()
        
        # Here, you would usually validate the input and create a Patient object
        # For demonstration, we'll just print the inputs
        print(first_name, last_name, identifier)

        self.clear_fields()

    def clear_fields(self):
        """Clears all input fields in the form."""
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.identifier_var.set("")

    def handle_return_key (self, event): #This will scroll through the widgets using <Return> for ease of use
        
        current_field = self.focus_get()

        if current_field in self.fields:
            current_index = self.fields.index(current_field)
            next_index = (current_index + 1) % len(self.fields) #Wraps around to the first field after 5
            self.fields[next_index].focus_set()



if __name__ == "__main__":
    app = PatientApp()
    app.mainloop()