import os
import shutil
# IMPORTANT NOTE: BENIGN_25K, MISLEADING AND PHISH_SAMPLE_25K folders must be put inside PhishIntention folder which is
# in the same directory with data_prepare.py


def move_html_files(src_folder, dest_folder):
    # Iterate through each folder in the misleading folder
    for folder_name in os.listdir(src_folder):
        folder_path = os.path.join(src_folder, folder_name)

        # Check if it's a directory
        if os.path.isdir(folder_path):
            # Check if the folder contains html.txt
            html_file_path = os.path.join(folder_path, 'html.txt')
            if os.path.exists(html_file_path):
                # Move the html.txt file to the legitimate folder
                dest_path = os.path.join(dest_folder, f"{folder_name}_html.txt")
                shutil.move(html_file_path, dest_path)
                print(f"Moved {folder_name}/html.txt to {dest_folder}")


# Set the paths for the misleading and legitimate folders
phish_intention_folder = os.path.join(os.getcwd(), 'PhishIntention')
misleading_folder = os.path.join(phish_intention_folder, 'misleading')
legitimate_folder = os.path.join(os.getcwd(), 'Legitimate')
illegitimate_folder = os.path.join(os.getcwd(), 'Phishing')
phish_folder = os.path.join(phish_intention_folder, 'phish_sample_30k')
benign_folder = os.path.join(phish_intention_folder, 'benign_25k')

# Create the legitimate folder if it doesn't exist
if not os.path.exists(legitimate_folder):
    os.makedirs(legitimate_folder)
if not os.path.exists(illegitimate_folder):
    os.makedirs(illegitimate_folder)

# Call the function to move html.txt files
move_html_files(misleading_folder, legitimate_folder)
move_html_files(benign_folder, legitimate_folder)
move_html_files(phish_folder, illegitimate_folder)
