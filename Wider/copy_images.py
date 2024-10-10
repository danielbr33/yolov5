import os
import shutil
import sys

# Supported image file extensions
image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}


def move_images_to_main_folder(main_folder):
    # Walk through all subdirectories
    for root, dirs, files in os.walk(main_folder):
        # Skip the main folder itself
        if root == main_folder:
            continue

        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension in image_extensions:
                # Full path of the image file
                file_path = os.path.join(root, file)
                # Destination path in the main folder
                dest_path = os.path.join(main_folder, file)

                # Check if file already exists in the main folder
                if os.path.exists(dest_path):
                    print(f"File {file} already exists in {main_folder}. Skipping.")
                else:
                    # Move the image to the main folder
                    shutil.move(file_path, dest_path)
                    print(f"Moved: {file_path} -> {dest_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]

    # Check if the provided path is valid
    if not os.path.exists(folder_path):
        print(f"Error: The folder {folder_path} does not exist.")
        sys.exit(1)

    # Run the image moving function
    move_images_to_main_folder(folder_path)
    print("All images have been moved to the main folder.")
