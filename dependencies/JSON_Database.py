import json
from datetime import datetime

def Json_Database_Initialization(Main_Name,Main_Name_Full_Path,
                             entry_date, entry_start_time,
                             Photo_List, Audio_List,
                             Database_Lieutenant_Path):
    
    end = datetime.now()
    entry_end_time = end.strftime("%H:%M:%S")
    data = { "Page1":
                {
                "Main Name": Main_Name,
                "Main Full path": Main_Name_Full_Path,
                "Date": entry_date,
                "writing start time": entry_start_time,
                "writing end time": entry_end_time,
                "Links": {
                    "Photo Link": Photo_List, # [] list
                    "Audio Link": Audio_List
                }
            }
        }
    with open(Database_Lieutenant_Path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print("JSON file created successfully.")


def clear_and_input_new_data(data, page_name, 
                             Main_Name, Main_Name_Full_Path,
                             edit_start_time, edit_end_time,
                             last_entry_date, Photo_List, Audio_List, 
                             Database_Lieutenant_Path):
    
    if page_name in data:
        # Save the existing "writing start time" and "writing end time"
        existing_start_time = data[page_name]["writing start time"]
        existing_end_time = data[page_name]["writing end time"]
        existing_entry_date = data[page_name]["Date"]
        # Clear existing data for the specified page
        data[page_name] = {}

        # Input new data similar to Json_Database_Initialization
        new_page_data = {
            "Main Name": Main_Name,
            "Main Full path": Main_Name_Full_Path,
            "Date": existing_entry_date,
            "Last Edit Date":  last_entry_date,
            "writing start time": existing_start_time,  
            "writing end time": existing_end_time,

            "Edit start time": edit_start_time,  
            "Edit end time": edit_end_time,            
            "Links": {
                "Photo Link": Photo_List,
                "Audio Link": Audio_List
            }
        }

        # Update the page with the new data
        data[page_name] = new_page_data

        # Save the modified data
        modify_and_save_json(Database_Lieutenant_Path, data)

        print(f"Data for page '{page_name}' cleared and new data input successfully.")
    else:
        print(f"Error: Page '{page_name}' not found in the database.")

def find_page_number(json_file, target_full_path):
    with open(json_file, 'r') as file:
        data = json.load(file)

    for page_number, page_info in data.items():
        if page_info.get("Main Full path") == target_full_path:
            return page_number

    return None

def Add_Page(data, Page_name,Main_Name, Main_Name_Full_Path , entry_date, entry_start_time, 
             Photo_List,Audio_List, Database_Lieutenant_Path):
    
    end = datetime.now()
    entry_end_time = end.strftime("%H:%M:%S")
    blank_Page = {
        "Main Name": Main_Name,
        "Main Full path": Main_Name_Full_Path,
        "Date": entry_date, 
        "writing start time": entry_start_time,
        "writing end time": entry_end_time,
        "Links": {
            "Photo Link": Photo_List, # [] list
            "Audio Link": Audio_List
        }
    }
    data[Page_name] = blank_Page

def read_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def modify_and_save_json(file_path, modified_data):
    with open(file_path, 'w') as json_file:
        json.dump(modified_data, json_file, indent=4)