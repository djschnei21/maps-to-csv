import json
import csv
import re
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to extract address, city, state, and zip from the URL
def extract_address_from_url(url):
    match = re.search(r'q=(.*?)(?:&|$)', url)
    if match:
        address = match.group(1).replace('+', ' ')
        parts = address.split(',')
        if len(parts) == 4:
            return parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3].strip()
        elif len(parts) == 3:
            # Assuming the format is address, city, state zip
            address = parts[0].strip()
            city = parts[1].strip()
            state_zip = parts[2].strip().split()
            if len(state_zip) == 2:
                state = state_zip[0]
                zip_code = state_zip[1]
                return address, city, state, zip_code
    return None, None, None, None

# Function to process the JSON file and write to CSV
def process_file(json_file_path, csv_file_path):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = ['salutation', 'firstname', 'lastname', 'fullname', 'address', 'city', 'state', 'zip', 'citystatezip']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for feature in data['features']:
                properties = feature['properties']
                address = None
                city = None
                state = None
                zip_code = None

                if 'location' in properties and 'address' in properties['location']:
                    address_parts = properties['location']['address'].split(',')
                    if len(address_parts) == 4:
                        address = address_parts[0].strip()
                        city = address_parts[1].strip()
                        state = address_parts[2].strip()
                        zip_code = address_parts[3].strip()
                    elif len(address_parts) == 3:
                        address = address_parts[0].strip()
                        city = address_parts[1].strip()
                        state_zip = address_parts[2].strip().split()
                        if len(state_zip) == 2:
                            state = state_zip[0]
                            zip_code = state_zip[1]
                else:
                    address, city, state, zip_code = extract_address_from_url(properties['google_maps_url'])

                if address and city and state and zip_code:
                    writer.writerow({'salutation': '','' 'firstname': '', 'lastname': "Preferred Customer", 'fullname': "Preferred Customer", 'address': address, 'city': city, 'state': state, 'zip': zip_code, 'citystatezip': f"{city} {state} {zip_code}"})
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# Function to open file dialog and select JSON file
def open_file_dialog():
    json_file_path = filedialog.askopenfilename(title="Select a JSON file", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if json_file_path:
        csv_file_path = filedialog.asksaveasfilename(title="Save CSV file as", defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if csv_file_path:
            success = process_file(json_file_path, csv_file_path)
            if success:
                messagebox.showinfo("Success", f"Addresses have been written to {csv_file_path}")
            else:
                messagebox.showerror("Error", "Failed to process the file")

# Create the main Tkinter window
root = tk.Tk()
root.title("Address Extractor")

# Create a label and a button to browse files
label = tk.Label(root, text="Click the button to browse and select a JSON file", font=('Arial', 12))
label.pack(pady=20)

browse_button = tk.Button(root, text="Browse", command=open_file_dialog, font=('Arial', 12))
browse_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()