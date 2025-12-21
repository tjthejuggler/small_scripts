
import os

# Data structure defining the sessions and the number of abstracts in each.
# This has been corrected to include session S5.
# Format: { 'SessionName': NumberOfAbstracts }
sessions_data = {
    'S1': 9,
    'S2': 6,
    'S3': 6,
    'S4': 6,
    'S5': 6,  # <-- Corrected: Added S5
    'OS1': 9,
    'OS2': 10,
    'OS3': 9,
    'OS4': 10,
}

# Get the directory where the script is located to create folders in the same place.
base_directory = os.getcwd()
print(f"Will create directories and files in: {base_directory}\n")

# --- Main loop to create directories and files ---

# Iterate over each session defined in our dictionary
for session_name, num_abstracts in sessions_data.items():
    
    # Define the path for the session directory
    session_path = os.path.join(base_directory, session_name)
    
    # Create the session directory.
    # The 'exist_ok=True' argument prevents an error if the directory already exists.
    try:
        os.makedirs(session_path, exist_ok=True)
        print(f"Created directory: {session_name}")
    except OSError as e:
        print(f"Error creating directory {session_name}: {e}")
        continue # Skip to the next session if directory creation fails

    # Loop from 1 to the total number of abstracts for this session
    for i in range(1, num_abstracts + 1):
        # Format the filename, e.g., "S1-1.md"
        file_name = f"{session_name}-{i}.md"
        
        # Create the full path for the file
        file_path = os.path.join(session_path, file_name)
        
        # Create an empty file by opening it in write mode ('w').
        # The 'with' statement ensures the file is properly closed.
        try:
            with open(file_path, 'w') as f:
                pass  # 'pass' does nothing, leaving the file empty
            print(f"  - Created file: {file_name}")
        except IOError as e:
            print(f"  - Error creating file {file_name}: {e}")
            
    print("-" * 20) # Separator for readability

print("\nScript finished successfully!")
