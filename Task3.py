import os
import shutil
from datetime import datetime
import zipfile

# Define the source folder (e.g., Downloads folder)
source_folder = r'C:\Users\das\Downloads'  # Using raw string

# Define destination folders with subfolders for some categories
destinations = {
    'Images': {
        'JPG': [r'C:\Users\das\Desktop\Organized Files\Images\JPG', ['.jpg']],
        'JPEG': [r'C:\Users\das\Desktop\Organized Files\Images\JPEG', ['.jpeg']],
        'PNG': [r'C:\Users\das\Desktop\Organized Files\Images\PNG', ['.png']],
        'GIF': [r'C:\Users\das\Desktop\Organized Files\Images\GIF', ['.gif']]
    },
    'Documents': {
        'Word Files': [r'C:\Users\das\Desktop\Organized Files\Documents\Word Files', ['.docx']],
        'PDF Files': [r'C:\Users\das\Desktop\Organized Files\Documents\PDF Files', ['.pdf']],
        'RTF Files': [r'C:\Users\das\Desktop\Organized Files\Documents\RTF Files', ['.rtf']],
    },
    'Archives': [r'C:\Users\das\Desktop\Organized Files\Archives', ['.zip', '.rar', '.7z']],
    'Audio': [r'C:\Users\das\Desktop\Organized Files\Audio', ['.mp3', '.wav', '.aac']],
    'Videos': [r'C:\Users\das\Desktop\Organized Files\Videos', ['.mp4', '.mov', '.avi']],
    'PPTs': [r'C:\Users\das\Desktop\Organized Files\PPTs', ['.ppt', '.pptx']]
}

# Create a log file to track moved files
log_file = r'C:\Users\das\Desktop\Organized Files\logfile.txt'

# Function to write to log
def write_log(message):
    with open(log_file, 'a') as log:
        log.write(f'{datetime.now()} - {message}\n')

# Function to unzip archives
def unzip_file(file_path, destination_folder):
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(destination_folder)
        os.remove(file_path)  # Remove the archive after extraction
        write_log(f'Unzipped {file_path} to {destination_folder}')
    except Exception as e:
        write_log(f'Failed to unzip {file_path}: {e}')

# Function to handle file duplication (renaming duplicates)
def move_file_with_duplication_check(src, dest):
    base, ext = os.path.splitext(dest)
    counter = 1
    while os.path.exists(dest):
        dest = f"{base}_{counter}{ext}"
        counter += 1
    try:
        write_log(f'Attempting to move {src} to {dest}')
        shutil.move(src, dest)
        write_log(f'Moved {src} to {dest}')
    except FileNotFoundError as e:
        write_log(f'FileNotFoundError: {e} for file {src} or destination {dest}')

# Function to organize files with enhanced features, ensuring proper order
def organize_files(source_folder):
    # Get all files in the source folder
    all_files = os.listdir(source_folder)
    
    # Handle categories with subfolders first (e.g., Images, Documents)
    for category, sub_folders in destinations.items():
        if isinstance(sub_folders, dict):  # Check if the category has subfolders
            for sub_folder, (dest_folder, extensions) in sub_folders.items():
                for filename in all_files:
                    file_path = os.path.join(source_folder, filename)

                    # Ignore temporary files (starting with ~$)
                    if filename.startswith('~$'):
                        write_log(f'Skipping temporary file: {filename}')
                        continue

                    # Check if the file exists
                    if os.path.isfile(file_path):
                        _, ext = os.path.splitext(filename)

                        # Move the file if its extension matches the current subfolder
                        if ext.lower() in extensions:
                            if not os.path.exists(dest_folder):
                                os.makedirs(dest_folder)
                                write_log(f'Created folder: {dest_folder}')
                            
                            destination_path = os.path.join(dest_folder, filename)
                            
                            # Handle duplicates by renaming the file
                            move_file_with_duplication_check(file_path, destination_path)
                            print(f'Moved {filename} to {sub_folder} in {category}')

                            # Remove file from the all_files list after processing
                            all_files.remove(filename)

    # Now handle the remaining categories without subfolders (e.g., PPTs, Audio, Videos)
    for category, content in destinations.items():
        if not isinstance(content, dict):  # For categories without subfolders
            dest_folder, extensions = content
            for filename in all_files:
                file_path = os.path.join(source_folder, filename)

                # Ignore temporary files (starting with ~$)
                if filename.startswith('~$'):
                    write_log(f'Skipping temporary file: {filename}')
                    continue

                # Check if the file exists
                if os.path.isfile(file_path):
                    _, ext = os.path.splitext(filename)

                    # Move the file if its extension matches the current category
                    if ext.lower() in extensions:
                        if not os.path.exists(dest_folder):
                            os.makedirs(dest_folder)
                            write_log(f'Created folder: {dest_folder}')
                        
                        destination_path = os.path.join(dest_folder, filename)
                        
                        # Handle duplicates by renaming the file
                        move_file_with_duplication_check(file_path, destination_path)
                        print(f'Moved {filename} to {category}')

                        # Unzip archives if the file is an archive
                        if category == 'Archives':
                            unzip_file(destination_path, dest_folder)
                        # Remove file from the all_files list after processing
                        all_files.remove(filename)

if __name__ == "__main__":
    organize_files(source_folder)
    write_log("File organization complete!")
    print("File organization complete!")
