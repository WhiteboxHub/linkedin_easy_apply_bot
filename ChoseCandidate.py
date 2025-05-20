import os
import yaml

def chooseCandidate(directory="configs"):
    
    yaml_files = [f for f in os.listdir(directory) if f.endswith('.yaml') or f.endswith('.yml')]
    
    # Check if there are any YAML files in the directory
    if not yaml_files:
        print("No YAML files found in the directory.")
        return
    
    # Print the list of YAML files with numbers
    for idx, file_name in enumerate(yaml_files, 1):
        print(f"{idx} = {file_name}")
    
    # Prompt user to select a file by number
    try:
        selected_number = int(input("Enter the number of the file you want to select: "))
        
        # Validate the input
        if 1 <= selected_number <= len(yaml_files):
            selected_file = yaml_files[selected_number - 1]
            file_path = os.path.join(directory, selected_file)
            
            # Print the full path of the selected file
            print(f"\nSelected File Path: {file_path}")
            
            return file_path
        else:
            print("Invalid selection. Please enter a number corresponding to the listed files.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")


# Example usage
directory_path = "configs"  



def getFull_path_Resume(path):

    relative_path = path.lstrip('/\\')

    #get current workingDirectory

    current_directory = os.getcwd()

    fullpath = os.path.join(current_directory,relative_path)
    fullpath = os.path.normpath(fullpath)
    if os.path.isfile(fullpath):
        print(fullpath, "is available ---------- Starting the bot.")
        
        return fullpath
    